import io
import logging

import pytest

from logger import get_logger, init_logging


@pytest.fixture(autouse=True)
def bare_root_logger():
    """init_logging is a no-op once the root logger has handlers."""
    root = logging.getLogger()
    saved_handlers, saved_level = root.handlers[:], root.level
    root.handlers.clear()
    yield
    for handler in root.handlers:
        handler.close()
    root.handlers[:] = saved_handlers
    root.setLevel(saved_level)


def test_log_lines_go_to_the_given_stream(capsys):
    stream = io.StringIO()
    init_logging(stream=stream)

    get_logger("app").info("synced 3 products")

    assert stream.getvalue() == "INFO     app — synced 3 products\n"
    assert capsys.readouterr().out == ""


def test_log_lines_go_to_stdout_when_no_stream_is_given(capsys):
    init_logging()

    get_logger("app").warning("disk almost full")

    captured = capsys.readouterr()
    assert captured.out == "WARNING  app — disk almost full\n"
    assert captured.err == ""


def test_lines_below_the_level_are_dropped():
    stream = io.StringIO()
    init_logging(level="WARNING", stream=stream)

    get_logger("app").info("noise")
    get_logger("app").error("broken")

    assert stream.getvalue() == "ERROR    app — broken\n"


def test_a_second_call_does_not_add_a_second_handler():
    first, second = io.StringIO(), io.StringIO()
    init_logging(stream=first)
    init_logging(stream=second)

    get_logger("app").info("once")

    assert (first.getvalue(), second.getvalue()) == ("INFO     app — once\n", "")


def test_the_log_file_gets_a_timestamped_line(tmp_path):
    log_file = tmp_path / "logs" / "app.log"
    init_logging(log_file=log_file, stream=io.StringIO())

    get_logger("app").info("written to file")

    line = log_file.read_text()
    assert "INFO     app test_the_log_file_gets_a_timestamped_line:" in line
    assert line.endswith("— written to file\n")

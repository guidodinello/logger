import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

_5MB = 5 * 1024 * 1024

_CONSOLE_FMT = "%(levelname)-8s %(name)s — %(message)s"
_FILE_FMT = "%(asctime)s %(levelname)-8s %(name)s %(funcName)s:%(lineno)d — %(message)s"

_COLORS = {
    logging.DEBUG: "\x1b[38;20m",
    logging.INFO: "\x1b[32m",
    logging.WARNING: "\x1b[33;20m",
    logging.ERROR: "\x1b[31;20m",
    logging.CRITICAL: "\x1b[31;1m",
}
_RESET = "\x1b[0m"


class _ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        color = _COLORS.get(record.levelno, "")
        formatter = logging.Formatter(color + _CONSOLE_FMT + _RESET, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def init_logging(log_file: Path | None = None, level: LogLevel = "INFO") -> None:
    """Configure the root logger. Call once at application startup.

    Installs a stdout StreamHandler and, if log_file is given, a 5 MB
    RotatingFileHandler (3 backups).  No-op if handlers are already set up.
    """
    root = logging.getLogger()
    if root.handlers:
        return

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(_ColorFormatter() if sys.stdout.isatty() else logging.Formatter(_CONSOLE_FMT))
    root.addHandler(sh)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(log_file, maxBytes=_5MB, backupCount=3)
        fh.setFormatter(logging.Formatter(_FILE_FMT, datefmt="%Y-%m-%d %H:%M:%S"))
        root.addHandler(fh)

    root.setLevel(level.upper())


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

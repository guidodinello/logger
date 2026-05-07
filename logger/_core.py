import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def init_logging(log_file: Path | None = None, level: str = "INFO") -> None:
    """Configure the root logger. Call once at application startup.

    Installs a stdout StreamHandler and, if log_file is given, a 5 MB
    RotatingFileHandler (3 backups).  No-op if handlers are already set up.
    """
    root = logging.getLogger()
    if root.handlers:
        return

    fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(name)s — %(message)s")

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    root.addHandler(sh)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        fh.setFormatter(fmt)
        root.addHandler(fh)

    root.setLevel(level.upper())


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

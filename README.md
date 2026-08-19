# logger

Minimal stdlib logging setup for Python projects — stdout + rotating file, one `init_logging()` call.

## Features

- Configures the root logger once at startup
- stdout `StreamHandler` always active
- Optional 5 MB `RotatingFileHandler` (3 backups)
- `get_logger(name)` — thin wrapper around `logging.getLogger`
- No dependencies beyond the stdlib

## Installation

```bash
uv pip install -e /path/to/logger
```

Or add it as a local dependency in `pyproject.toml`:

```toml
[project]
dependencies = [
    "logger @ file:///path/to/logger",
]
```

Requires Python 3.13+.

## Usage

Call `init_logging()` once at application startup (e.g. in `main()`), then use
`get_logger(__name__)` in every module:

```python
from logger import get_logger, init_logging
from pathlib import Path


def main() -> None:
    init_logging(log_file=Path("logs/app.log"), level="DEBUG")
    log = get_logger(__name__)
    log.info("started")
```

```python
# any other module
from logger import get_logger

log = get_logger(__name__)


def do_work() -> None:
    log.info("processing %d items", count)
```

### `init_logging(log_file, level)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `log_file` | `Path \| None` | `None` | Path for the rotating log file. Omit for stdout only. |
| `level` | `str` | `"INFO"` | Root log level (`"DEBUG"`, `"INFO"`, `"WARNING"`, …). |

No-op if the root logger already has handlers — safe to call in tests or libraries that
call `init_logging` themselves.

### Log format

```
2025-05-06 12:34:56,789 INFO     myapp.core — message here
```

## Development

```bash
uv run ruff check --fix .   # lint
```

from __future__ import annotations

import logging
from pathlib import Path


def setup_logger(log_path: str | Path) -> logging.Logger:
    """Configure and return a logger that writes to the given path."""
    logger = logging.getLogger("pdf_processor")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter(
        "% (asctime)s - %(levelname)s - %(message)s".replace("%", "%%")
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


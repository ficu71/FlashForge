"""Thin wrapper around Python's logging module with a per‑class singleton pattern.

Logger also supports sending log messages to a GUI handler if one is set.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Optional


class Logger:
    _instances: Dict[str, logging.Logger] = {}
    _gui_handler: Optional[Callable[[str], None]] = None

    def __init__(self, name: str) -> None:
        if name not in Logger._instances:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%Y-%m-%d %H:%M:%S - %(name)s - %(levelname)s - %(message)s"
            )
            # Ensure logs directory exists
            Path("logs").mkdir(parents=True, exist_ok=True)
            log_filename = f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_filename)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            # Output to console as well
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            Logger._instances[name] = logger
        self.logger = Logger._instances[name]

    @staticmethod
    def set_gui_handler(handler: Callable[[str], None]) -> None:
        """Register a handler that will receive log messages for GUI display."""
        Logger._gui_handler = handler

    def info(self, message: str) -> None:
        self.logger.info(message)
        if Logger._gui_handler:
            Logger._gui_handler(f"[INFO] {message}")

    def error(self, message: str) -> None:
        self.logger.error(message)
        if Logger._gui_handler:
            Logger._gui_handler(f"[ERROR] {message}")

    def warning(self, message: str) -> None:
        self.logger.warning(message)
        if Logger._gui_handler:
            Logger._gui_handler(f"[WARNING] {message}")
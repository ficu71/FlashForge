"""Log view that subscribes to global log messages and shows them in a QTextEdit."""

from PyQt5.QtWidgets import QTextEdit
from utils.logger import Logger


class LogView(QTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.setReadOnly(True)
        # Register a GUI handler so all log messages show up here
        Logger.set_gui_handler(self.append_log)

    def append_log(self, message: str) -> None:
        self.append(message)
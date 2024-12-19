from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt


class ConsoleWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def log(self, message):
        """Добавление сообщения в консоль"""
        self.append(message)
        # Прокручиваем к последнему сообщению
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum()
        )

    def clear_console(self):
        """Очистка консоли"""
        self.clear()

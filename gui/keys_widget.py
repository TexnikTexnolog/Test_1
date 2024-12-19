from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal


class KeysWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.available_keys = []  # Список доступных клавиш
        self.init_ui()

    def set_available_keys(self, keys):
        """Установка списка доступных клавиш"""
        self.available_keys = keys

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Создаем контейнер для клавиш
        self.keys_layout = QVBoxLayout()
        self.keys_layout.setSpacing(8)
        layout.addLayout(self.keys_layout)

        # Кнопки управления клавишами
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        self.add_key_btn = QPushButton('Добавить клавишу')
        self.remove_key_btn = QPushButton('Удалить клавишу')

        # Применяем стиль к кнопкам
        button_style = """
            QPushButton {
                background-color: #404040;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px 15px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """
        self.add_key_btn.setStyleSheet(button_style)
        self.remove_key_btn.setStyleSheet(button_style)

        buttons_layout.addWidget(self.add_key_btn)
        buttons_layout.addWidget(self.remove_key_btn)
        layout.addLayout(buttons_layout)

        # Подключаем сигналы
        self.add_key_btn.clicked.connect(self.add_key_row)
        self.remove_key_btn.clicked.connect(self.remove_key_row)

    def add_key_row(self):
        """Добавление строки с настройками клавиши"""
        row_layout = QHBoxLayout()
        row_layout.setSpacing(8)

        key_combo = QComboBox()
        key_combo.addItems(self.available_keys)
        min_delay = QSpinBox()
        max_delay = QSpinBox()

        min_delay.setRange(0, 10000)
        max_delay.setRange(0, 10000)

        row_layout.addWidget(QLabel('Клавиша:'))
        row_layout.addWidget(key_combo)
        row_layout.addWidget(QLabel('Период мин (мс):'))
        row_layout.addWidget(min_delay)
        row_layout.addWidget(QLabel('Период макс (мс):'))
        row_layout.addWidget(max_delay)

        self.keys_layout.insertLayout(self.keys_layout.count(), row_layout)

    def remove_key_row(self):
        """Удаление последней строки с настройками клавиши"""
        if self.keys_layout.count() > 0:
            layout = self.keys_layout.takeAt(self.keys_layout.count() - 1)
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                layout.deleteLater()

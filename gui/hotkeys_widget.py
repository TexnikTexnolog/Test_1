from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QCheckBox)
from PyQt5.QtCore import Qt


class HotkeysWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Старт
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel('Клавиша для запуска:'))
        self.start_key_combo = QComboBox()
        self.start_ctrl_check = QCheckBox('Ctrl')
        self.start_alt_check = QCheckBox('Alt')
        start_layout.addWidget(self.start_key_combo)
        start_layout.addWidget(self.start_ctrl_check)
        start_layout.addWidget(self.start_alt_check)
        layout.addLayout(start_layout)

        # Стоп
        stop_layout = QHBoxLayout()
        stop_layout.addWidget(QLabel('Клавиша для остановки:'))
        self.stop_key_combo = QComboBox()
        self.stop_ctrl_check = QCheckBox('Ctrl')
        self.stop_alt_check = QCheckBox('Alt')
        stop_layout.addWidget(self.stop_key_combo)
        stop_layout.addWidget(self.stop_ctrl_check)
        stop_layout.addWidget(self.stop_alt_check)
        layout.addLayout(stop_layout)

        # Кнопки управления
        control_layout = QHBoxLayout()
        self.start_btn = QPushButton('Запуск скрипта')
        self.stop_btn = QPushButton('Стоп скрипт')
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        layout.addLayout(control_layout)

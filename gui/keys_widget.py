from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QSpinBox)
from PyQt5.QtCore import Qt


class KeysWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                border: none;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Создаем заголовок
        header = QWidget()
        header.setFixedHeight(25)
        header.setStyleSheet("""
            QWidget {
                background-color: #404040;
                border: none;
                border-radius: 5px;
            }
            QWidget:hover {
                background-color: #505050;
            }
        """)
        header.setCursor(Qt.PointingHandCursor)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 5, 0)

        # Добавля��м текст напрямую через QLabel
        title_label = QLabel('Клавиши')
        title_label.setStyleSheet("""
            QLabel {
                background: transparent;
                color: white;
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Кнопка сворачивания
        self.toggle_btn = QPushButton("▼")
        self.toggle_btn.setFixedSize(30, 25)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 10px;
            }
        """)
        header_layout.addWidget(self.toggle_btn)

        # Создаем контейнер для содержимого
        self.content = QWidget()
        self.content.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
            }
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
            QComboBox, QSpinBox {
                background-color: #404040;
                border: none;
                border-radius: 3px;
                color: white;
                padding: 3px;
                min-width: 60px;
            }
        """)

        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(8)

        # Layout для клавиш
        self.keys_layout = QVBoxLayout()
        self.keys_layout.setSpacing(8)
        content_layout.addLayout(self.keys_layout)

        # Кнопки управления клавишами
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        self.add_key_btn = QPushButton('Добавить клавишу')
        self.remove_key_btn = QPushButton('Удалить клавишу')

        buttons_layout.addWidget(self.add_key_btn)
        buttons_layout.addWidget(self.remove_key_btn)
        content_layout.addLayout(buttons_layout)

        # Добавляем компоненты в основной layout
        layout.addWidget(header)
        layout.addWidget(self.content)

        # Подключаем сигналы
        self.toggle_btn.clicked.connect(self.toggle_content)
        header.mousePressEvent = lambda e: self.toggle_content()
        self.add_key_btn.clicked.connect(self.add_key_row)
        self.remove_key_btn.clicked.connect(self.remove_key_row)

    def toggle_content(self):
        """Сворачивание/разворачивание содержимого"""
        if self.content.isVisible():
            self.content.hide()
            self.toggle_btn.setText("▼")
            self.setFixedHeight(25)
        else:
            self.content.show()
            self.toggle_btn.setText("▲")
            self.setMinimumHeight(0)
            self.setMaximumHeight(16777215)

    def add_key_row(self):
        """Добавление строки с настройками клавиши"""
        row_layout = QHBoxLayout()
        row_layout.setSpacing(8)

        key_combo = QComboBox()
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

    def set_available_keys(self, keys):
        """Установка списка доступных клавиш"""
        self.available_keys = keys

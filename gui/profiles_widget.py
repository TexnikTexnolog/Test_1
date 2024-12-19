from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QComboBox)
from PyQt5.QtCore import Qt
from core.window_capture import WindowCapture


class ProfilesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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

        # Добавляем текст напрямую через QLabel
        title_label = QLabel('Настройки профиля')
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

        # Контент профилей
        self.content = QWidget()
        self.content.setMinimumHeight(150)
        self.content.setMaximumHeight(150)
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setSpacing(5)

        # Профили
        profiles_layout = QHBoxLayout()
        self.new_profile_edit = QLineEdit()
        self.new_profile_edit.setPlaceholderText('Введите имя нового профиля')
        self.save_profile_btn = QPushButton('Сохранить профиль')
        profiles_layout.addWidget(self.new_profile_edit)
        profiles_layout.addWidget(self.save_profile_btn)
        content_layout.addLayout(profiles_layout)

        # Управление профилями
        profile_controls = QHBoxLayout()
        self.profile_combo = QComboBox()
        self.load_profile_btn = QPushButton('Загрузить профиль')
        self.update_profile_btn = QPushButton('Обновить профиль')
        self.delete_profile_btn = QPushButton('Удалить профиль')
        profile_controls.addWidget(self.profile_combo)
        profile_controls.addWidget(self.load_profile_btn)
        profile_controls.addWidget(self.update_profile_btn)
        profile_controls.addWidget(self.delete_profile_btn)
        content_layout.addLayout(profile_controls)

        # Выбор окна
        window_layout = QHBoxLayout()
        self.window_combo = QComboBox()
        self.refresh_btn = QPushButton('Обновить список окон')
        window_layout.addWidget(QLabel('Окно:'))
        window_layout.addWidget(self.window_combo)
        window_layout.addWidget(self.refresh_btn)
        content_layout.addLayout(window_layout)

        # Выбор метода нажатий
        input_method_layout = QHBoxLayout()
        input_method_layout.addWidget(QLabel('Метод нажатий:'))
        self.input_method_combo = QComboBox()
        self.input_method_combo.addItems(['Arduino', 'Виртуальные нажатия'])
        input_method_layout.addWidget(self.input_method_combo)
        content_layout.addLayout(input_method_layout)

        # Настройки Arduino
        self.arduino_settings = QWidget()
        arduino_layout = QHBoxLayout(self.arduino_settings)
        arduino_layout.setContentsMargins(0, 0, 0, 0)
        arduino_layout.addWidget(QLabel('Порт Arduino (например, COM5):'))
        self.port_edit = QLineEdit()
        arduino_layout.addWidget(self.port_edit)
        content_layout.addWidget(self.arduino_settings)

        # Настраиваем размеры
        self.window_combo.setMaximumWidth(200)
        self.input_method_combo.setMaximumWidth(150)
        self.port_edit.setMaximumWidth(100)

        # Подключаем сигналы
        self.refresh_btn.clicked.connect(self.refresh_windows)
        self.input_method_combo.currentTextChanged.connect(
            self.on_input_method_changed)
        self.toggle_btn.clicked.connect(self.toggle_content)
        header.mousePressEvent = lambda e: self.toggle_content()

        # Добавляем растягивающийся элемент в конец,
        # чтобы прижать содержимое к верху
        content_layout.addStretch()

        layout.addWidget(header)
        layout.addWidget(self.content)

        # Устанавливаем начальные размеры виджета
        self.setMinimumHeight(175)  # header (25) + content (150)
        self.setMaximumHeight(175)  # header (25) + content (150)

    def refresh_windows(self):
        """Обновление списка окон"""
        self.window_combo.clear()
        windows = WindowCapture.get_window_list()
        window_titles = [title for title, _ in windows]
        self.window_combo.addItems(window_titles)

    def on_input_method_changed(self, method):
        """Обработка изменения метода нажатий"""
        if method == 'Arduino':
            self.arduino_settings.show()
        else:
            self.arduino_settings.hide()

    def toggle_content(self):
        """Сворачивание/разворачивание содержимого"""
        if self.content.isVisible():
            self.content.hide()
            self.toggle_btn.setText("▼")
            self.setFixedHeight(25)
        else:
            self.content.show()
            self.toggle_btn.setText("▲")
            self.setMinimumHeight(175)
            self.setMaximumHeight(175)

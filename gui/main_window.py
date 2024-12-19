from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QComboBox, QPushButton, QLabel, QLineEdit,
                             QSpinBox, QCheckBox, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from gui.console_widget import ConsoleWidget
from core.window_capture import WindowCapture
from gui.theme_switch import ThemeSwitch
from gui.profiles_widget import ProfilesWidget
from gui.hotkeys_widget import HotkeysWidget
from gui.keys_widget import KeysWidget
from gui.control_widget import ControlWidget
import json


# В начале файла добавим стили для тем
LIGHT_THEME = """
    QMainWindow, QWidget {
        background-color: #f0f0f0;
        color: #000000;
    }
    QPushButton {
        background-color: #e0e0e0;
        border: 1px solid #b0b0b0;
        padding: 5px;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #d0d0d0;
    }
    QLineEdit, QComboBox, QSpinBox {
        background-color: white;
        border: 1px solid #b0b0b0;
        padding: 3px;
    }
"""

DARK_THEME = """
    QMainWindow, QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    QPushButton {
        background-color: #3b3b3b;
        border: 1px solid #505050;
        padding: 5px;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #454545;
    }
    QLineEdit, QComboBox, QSpinBox {
        background-color: #3b3b3b;
        border: 1px solid #505050;
        padding: 3px;
        color: white;
    }
    QComboBox QAbstractItemView {
        background-color: #3b3b3b;
        color: white;
    }
"""


class ConsoleHeader(QWidget):
    def __init__(self, parent=None, toggle_callback=None):
        super().__init__(parent)
        self.toggle_callback = toggle_callback
        self.setFixedHeight(15)
        self.setStyleSheet("""
            QWidget {
                background-color: #404040;
                border-top: 1px solid #505050;
            }
            QWidget:hover {
                background-color: #505050;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if self.toggle_callback:
            self.toggle_callback()


class MainWindow(QMainWindow):
    def __init__(self, profile_manager):
        super().__init__()

        # Список доступных клавиш
        self.available_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                               'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                               'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                               'u', 'v', 'w', 'x', 'y', 'z',
                               'f1', 'f2', 'f3', 'f4', 'f5', 'f6',
                               'f7', 'f8', 'f9', 'f10', 'f11', 'f12']

        self.profile_manager = profile_manager
        self.init_ui()
        self.load_settings()  # Загружаем сохраненные настройки

    def init_ui(self):
        self.setWindowTitle('Настройки автоматического нажатия клавиш')
        self.setMinimumSize(480, 500)

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # ========== ВЕРХНЯЯ ПАНЕЛЬ ==========
        # Содержит переключатель темы и чекбокс "Поверх всех окон"
        header_layout = QHBoxLayout()
        self.theme_switch = ThemeSwitch()
        self.theme_switch.switched.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_switch)
        header_layout.addStretch()
        self.pin_window_check = QCheckBox('Поверх всех окон')
        self.pin_window_check.stateChanged.connect(self.toggle_window_pin)
        header_layout.addWidget(self.pin_window_check)
        main_layout.addLayout(header_layout)

        # Маленький отступ после шапки
        spacer = QWidget()
        spacer.setFixedHeight(0)
        main_layout.addWidget(spacer)

        # ========== БЛОК НАСТРОЕК ПРОФИЛЯ ==========
        # Содержит управление профилями, выбор окна и метода ввода
        self.profiles_widget = ProfilesWidget()
        main_layout.addWidget(self.profiles_widget)

        # ========== БЛОК НАСТРОЕК КЛАВИШ ==========
        # Здесь будут настройки клавиш и задержек
        self.keys_widget = KeysWidget()
        main_layout.addWidget(self.keys_widget)

        # ========== БЛОК УПРАВЛЕНИЯ ==========
        # Фиксированный блок с кнопками запуска/остановки и горячими клавишами
        bottom_container = QWidget()
        bottom_container.setFixedHeight(150)
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(5, 5, 5, 5)
        bottom_layout.setSpacing(5)

        self.control_widget = ControlWidget()
        bottom_layout.addWidget(self.control_widget)
        main_layout.addWidget(bottom_container)

        # ========== КОНСОЛЬ ==========
        # Сворачиваемая консоль для вывода логов
        self.console = ConsoleWidget()
        self.console.setMaximumHeight(75)
        console_container = QWidget()
        console_layout = QVBoxLayout(console_container)
        console_layout.setContentsMargins(0, 0, 0, 0)
        console_layout.setSpacing(0)

        # Заголовок консоли с кнопкой сворачивания
        header = ConsoleHeader(toggle_callback=self.toggle_console)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(5, 0, 5, 0)
        header_layout.addStretch()

        self.toggle_console_btn = QPushButton("▼")
        self.toggle_console_btn.setFixedSize(30, 15)
        self.toggle_console_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 10px;
                margin-top: -1px;
                padding: 0px;
            }
        """)
        header_layout.addWidget(self.toggle_console_btn)
        header_layout.addStretch()

        console_layout.addWidget(header)
        console_layout.addWidget(self.console)
        main_layout.addWidget(console_container)

        # Подключаем сигналы и настраиваем размеры
        self.toggle_console_btn.clicked.connect(self.toggle_console)
        self.control_widget.start_btn.setFixedHeight(30)
        self.control_widget.stop_btn.setFixedHeight(30)
        self.control_widget.start_btn.setMaximumWidth(120)
        self.control_widget.stop_btn.setMaximumWidth(120)

        # Заполняем комбобоксы доступными клавишами
        self.control_widget.start_key_combo.addItems(self.available_keys)
        self.control_widget.stop_key_combo.addItems(self.available_keys)

        # Загружаем начальные данные
        self.load_initial_data()

    def connect_signals(self):
        """Подключение сигналов к слотам"""
        self.profiles_widget.input_method_combo.currentTextChanged.connect(
            self.on_input_method_changed)

    def load_initial_data(self):
        """Загрузка начальных данных"""
        # Загрузка списка окон
        self.profiles_widget.refresh_windows()  # Вызываем метод из ProfilesWidget

        # Загрузка списка профилей
        self.refresh_profiles()

        # Загрузка последнего профиля
        if self.profile_manager.current_profile:
            self.load_profile_data(self.profile_manager.current_profile)

    def add_key_row(self):
        """обавление строки с настройками клавиши"""
        row_layout = QHBoxLayout()

        key_combo = QComboBox()
        key_combo.addItems(self.available_keys)  # Используем список клавиш
        min_delay = QSpinBox()
        max_delay = QSpinBox()

        min_delay.setRange(0, 10000)
        max_delay.setRange(0, 10000)

        row_layout.addWidget(QLabel('Клавиша:'))
        row_layout.addWidget(key_combo)
        row_layout.addWidget(QLabel('Период мин (мс):'))
        row_layout.addWidget(min_delay)
        row_layout.addWidget(QLabel('Период макс ():'))
        row_layout.addWidget(max_delay)

        self.keys_layout.addLayout(row_layout)

    def remove_key_row(self):
        """Удаление последнй строки с астрйками кавиши"""
        if self.keys_layout.count() > 0:
            layout = self.keys_layout.takeAt(self.keys_layout.count() - 1)
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                layout.deleteLater()

    def refresh_profiles(self):
        """Обновление списка профилей"""
        self.profiles_widget.profile_combo.clear()
        profiles = self.profile_manager.config.get_profiles_list()
        self.profiles_widget.profile_combo.addItems(profiles)

    def save_profile(self):
        """Сохранение новго профиля"""
        new_profile_name = self.profiles_widget.new_profile_edit.text().strip()
        if not new_profile_name:
            self.console.log("Ошибка: Введите имя нового профиля")
            return

        # Проверяем, существует ��и профиль
        existing_profiles = self.profile_manager.config.get_profiles_list()
        if new_profile_name in existing_profiles:
            self.console.log(f"Ошибка: Профиль {
                             new_profile_name} уже существует")
            return

        # обираем данные пофия
        keys = []
        for i in range(self.keys_layout.count()):
            layout = self.keys_layout.itemAt(i)
            if layout:
                widgets = [layout.itemAt(j).widget()
                           for j in range(layout.count())]
                key_data = {
                    'key': widgets[1].currentText(),
                    'min_delay': widgets[3].value(),
                    'max_delay': widgets[5].value()
                }
                keys.append(key_data)

        profile = {
            'name': new_profile_name,
            'window_title': self.profiles_widget.window_combo.currentText(),
            'input_method': self.profiles_widget.input_method_combo.currentText(),
            'arduino_port': self.profiles_widget.port_edit.text(),
            'keys': keys,
            'start_hotkey': {
                'key': self.hotkeys_widget.start_key_combo.currentText(),
                'ctrl': self.hotkeys_widget.start_ctrl_check.isChecked(),
                'alt': self.hotkeys_widget.start_alt_check.isChecked()
            },
            'stop_hotkey': {
                'key': self.hotkeys_widget.stop_key_combo.currentText(),
                'ctrl': self.hotkeys_widget.stop_ctrl_check.isChecked(),
                'alt': self.hotkeys_widget.stop_alt_check.isChecked()
            }
        }

        self.profile_manager.save_profile(profile)
        self.console.log(f"Профиль {new_profile_name} сохранен")
        self.new_profile_edit.clear()
        self.refresh_profiles()

    def load_profile(self):
        """Загрузка выбранного профиля"""
        profile_name = self.profiles_widget.profile_combo.currentText()
        if not profile_name:
            return

        if self.profile_manager.load_profile(profile_name):
            self.load_profile_data(self.profile_manager.current_profile)
            self.console.log(f"Профиль {profile_name} загружен")
        else:
            self.console.log(f"Ошибка згрузки профиля {profile_name}")

    def delete_profile(self):
        """Удаление выбранного профиля"""
        profile_name = self.profiles_widget.profile_combo.currentText()
        if not profile_name:
            return

        self.profile_manager.config.delete_profile(profile_name)
        self.console.log(f"Профиль {profile_name} удален")
        self.refresh_profiles()

    def start_script(self):
        """Запуск скрипта"""
        # TODO: Реализоват запуск скрпта
        self.console.log("Скрипт запущн")

    def stop_script(self):
        """становка скипта"""
        # TODO: Реалзоваь остановку скрипта
        self.console.log("Скрипт остановлен")

    def load_profile_data(self, profile):
        """агрузка даннх профиля в интерфейс"""
        # Очищаем текущий оля с клавишами
        while self.keys_layout.count():
            self.remove_key_row()

        # Устанавливаем значения в ProfilesWidget
        self.profiles_widget.window_combo.setCurrentText(profile.window_title)
        self.profiles_widget.input_method_combo.setCurrentText(
            profile.input_method)
        self.profiles_widget.port_edit.setText(profile.arduino_port)

        # Добавляем клавиши
        for key_config in profile.keys:
            self.add_key_row()
            row_idx = self.keys_layout.count() - 1
            row_layout = self.keys_layout.itemAt(row_idx)
            if row_layout:
                widgets = [row_layout.itemAt(j).widget()
                           for j in range(row_layout.count())]
                # ComboBox с клавишей
                widgets[1].setCurrentText(key_config.key)
                # SpinBox с мин. задержкой
                widgets[3].setValue(key_config.min_delay)
                # SpinBox с макс. задержкой
                widgets[5].setValue(key_config.max_delay)

        # Устанавливаем горячие клавиши
        self.hotkeys_widget.start_key_combo.setCurrentText(
            profile.start_hotkey['key'])
        self.hotkeys_widget.start_ctrl_check.setChecked(
            profile.start_hotkey['ctrl'])
        self.hotkeys_widget.start_alt_check.setChecked(
            profile.start_hotkey['alt'])

        self.hotkeys_widget.stop_key_combo.setCurrentText(
            profile.stop_hotkey['key'])
        self.hotkeys_widget.stop_ctrl_check.setChecked(
            profile.stop_hotkey['ctrl'])
        self.hotkeys_widget.stop_alt_check.setChecked(
            profile.stop_hotkey['alt'])

    def update_profile(self):
        """Обновление существующего профиля"""
        profile_name = self.profiles_widget.profile_combo.currentText()
        if not profile_name:
            self.console.log("Ошибка: Выберит профиль для обновления")
            return

        # Собираем данные прфиля
        keys = []
        for i in range(self.keys_layout.count()):
            layout = self.keys_layout.itemAt(i)
            if layout:
                widgets = [layout.itemAt(j).widget()
                           for j in range(layout.count())]
                key_data = {
                    'key': widgets[1].currentText(),
                    'min_delay': widgets[3].value(),
                    'max_delay': widgets[5].value()
                }
                keys.append(key_data)

        profile = {
            'name': profile_name,
            'window_title': self.profiles_widget.window_combo.currentText(),
            'input_method': self.profiles_widget.input_method_combo.currentText(),
            'arduino_port': self.profiles_widget.port_edit.text(),
            'keys': keys,
            'start_hotkey': {
                'key': self.hotkeys_widget.start_key_combo.currentText(),
                'ctrl': self.hotkeys_widget.start_ctrl_check.isChecked(),
                'alt': self.hotkeys_widget.start_alt_check.isChecked()
            },
            'stop_hotkey': {
                'key': self.hotkeys_widget.stop_key_combo.currentText(),
                'ctrl': self.hotkeys_widget.stop_ctrl_check.isChecked(),
                'alt': self.hotkeys_widget.stop_alt_check.isChecked()
            }
        }

        self.profile_manager.save_profile(profile)
        self.console.log(f"Профиль {profile_name} обновлен")
        self.refresh_profiles()

    def toggle_theme(self, is_dark: bool):
        """Переключение темы"""
        if is_dark:
            self.setStyleSheet(DARK_THEME)
            self.console.setStyleSheet(
                "background-color: #1b1b1b; color: #FFFFFF;")
        else:
            self.setStyleSheet(LIGHT_THEME)
            self.console.setStyleSheet(
                "background-color: #ffffff; color: #000000;")

        # Сохраняем настройку темы
        self.save_theme_setting(is_dark)

    def save_theme_setting(self, is_dark: bool):
        """Сохранене настройки темы"""
        settings_path = self.profile_manager.config.config_dir / "settings.json"
        settings = {}
        if settings_path.exists():
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)

        settings['dark_theme'] = is_dark

        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f)

    def load_settings(self):
        """Загрузка всех настроек"""
        settings_path = self.profile_manager.config.config_dir / "settings.json"
        if settings_path.exists():
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Згружаем тему
                is_dark = settings.get('dark_theme', True)
                self.theme_switch.set_theme(is_dark)
                self.toggle_theme(is_dark)

                # Загружаем состояние закрепления окна
                is_pinned = settings.get(
                    'window_pinned', False)  # по умолчанию False
                self.pin_window_check.setChecked(is_pinned)
                # toggle_window_pin будет взван автоматичк чрез сигнал

    def toggle_window_pin(self, state):
        """ереключение закрепления окна поверх остальных"""
        if state == Qt.Checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.console.log("Окно закреплено поверх остальных")
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.console.log("Окно отреплено")

        # Сохраняем состояние чекбокса
        self.save_window_pin_setting(state == Qt.Checked)
        self.show()  # Нужно пересодать окно после изменения флагов

    def save_window_pin_setting(self, is_pinned: bool):
        """Сохранение настройки закрепления окна"""
        settings_path = self.profile_manager.config.config_dir / "settings.json"
        settings = {}
        if settings_path.exists():
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)

        settings['window_pinned'] = is_pinned

        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f)

    def resizeEvent(self, event):
        """Обрботка изменния азмера она"""
        super().resizeEvent(event)
        # Здес можно добавить дополнительную логику при изменении размера

    def toggle_console(self):
        """Сворачивание/разворачивание консоли"""
        if self.console.isVisible():
            self.console.hide()
            self.toggle_console_btn.setText("▲")
        else:
            self.console.show()
            self.toggle_console_btn.setText("▼")

    def on_input_method_changed(self, method):
        """Обработка изменени�� метода нажатий"""
        if method == 'Arduino':
            # Используем arduino_settings из ProfilesWidget
            self.profiles_widget.arduino_settings.show()
            self.console.log("Выбран метод нажатий через Arduino")
        else:
            self.profiles_widget.arduino_settings.hide()
            self.console.log("Выбран метод виртуальных ажатий")

    # стальные методы будут реализованы позже

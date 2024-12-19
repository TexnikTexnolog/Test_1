from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import (Qt, pyqtSignal, QPropertyAnimation,
                          QRect, pyqtProperty)
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush


class ThemeSwitch(QWidget):
    switched = pyqtSignal(bool)  # Сигнал изменения состояния

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 28)

        # Инициализация переменных
        self._enabled = True
        self._state = True  # True = темная тема (по умолчанию)
        self._handle_position = 4  # Начальная позиция ползунка

        # Иконки
        self.moon = "🌙"
        self.sun = "☀️"

        # Настройка анимации после инициализации всех переменных
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setDuration(150)

    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Константы для размеров
        HANDLE_WIDTH = 20
        HANDLE_MARGIN = 4
        LEFT_POS = HANDLE_MARGIN  # 4
        RIGHT_POS = self.width() - HANDLE_WIDTH - HANDLE_MARGIN  # 36

        # Рисуем фон
        track_opacity = 0.6 if self._enabled else 0.3
        track_color = QColor(
            53, 53, 53) if self._state else QColor(200, 200, 200)
        track_color.setAlphaF(track_opacity)
        painter.setBrush(track_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)

        # Рисуем ползунок
        handle_opacity = 1.0 if self._enabled else 0.5
        handle_color = QColor(255, 255, 255)
        handle_color.setAlphaF(handle_opacity)
        painter.setBrush(handle_color)
        x = int(self._handle_position)
        painter.drawEllipse(x, HANDLE_MARGIN, HANDLE_WIDTH, HANDLE_WIDTH)

        # Рисуем иконки
        painter.setPen(QPen(Qt.white if self._state else Qt.black))

        # Получаем метрики для текста
        font_metrics = painter.fontMetrics()
        moon_width = font_metrics.horizontalAdvance(self.moon)
        sun_width = font_metrics.horizontalAdvance(self.sun)
        text_height = font_metrics.height()

        # Вычисляем координаты для центрирования
        # Небольшая корректировка по вертикали
        y = (self.height() + text_height) // 2 - 2

        # Центрируем иконки в своих половинах переключателя
        moon_x = (LEFT_POS + HANDLE_WIDTH // 2) - moon_width // 2
        sun_x = (RIGHT_POS + HANDLE_WIDTH // 2) - sun_width // 2

        # Рисуем иконки с центрированием
        painter.drawText(moon_x, y, self.moon)  # Луна слева
        painter.drawText(sun_x, y, self.sun)    # Солнце справа

        painter.end()

    def mousePressEvent(self, event):
        if self._enabled:
            self._state = not self._state
            self.animate_handle()
            self.switched.emit(self._state)

    def animate_handle(self):
        self.animation.setStartValue(self._handle_position)
        # Используем те же константы
        self.animation.setEndValue(4 if self._state else 36)
        self.animation.start()

    def is_dark_theme(self):
        return self._state

    def set_theme(self, is_dark: bool):
        if self._state != is_dark:
            self._state = is_dark
            self.animate_handle()
            self.update()

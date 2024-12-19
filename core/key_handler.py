import random
import time
from typing import Dict, List
import keyboard
from .arduino_controller import ArduinoController


class KeyHandler:
    def __init__(self, arduino_controller: ArduinoController):
        self.arduino = arduino_controller
        self.running = False
        self.key_timers: Dict[str, float] = {}
        self.key_configs: List[dict] = []

    def set_key_configs(self, configs: List[dict]):
        """Установка конфигурации клавиш"""
        self.key_configs = configs

    def start(self):
        """Запуск обработчика клавиш"""
        self.running = True
        self.key_timers = {cfg['key']: 0 for cfg in self.key_configs}

    def stop(self):
        """Остановка обработчика клавиш"""
        self.running = False
        # Отпускаем все клавиши
        for key in self.key_timers.keys():
            self.arduino.release_key(key)

    def process(self):
        """Обработка нажатий клавиш"""
        if not self.running:
            return

        current_time = time.time()

        for config in self.key_configs:
            key = config['key']
            min_delay = config['min_delay'] / 1000  # конвертируем мс в секунды
            max_delay = config['max_delay'] / 1000

            if current_time - self.key_timers[key] >= random.uniform(min_delay, max_delay):
                # Нажимаем клавишу
                self.arduino.press_key(key)
                # Небольшая задержка для имитации реального нажатия
                time.sleep(0.05)
                # Отпускаем клавишу
                self.arduino.release_key(key)
                # Обновляем таймер
                self.key_timers[key] = current_time

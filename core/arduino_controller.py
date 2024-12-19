try:
    import serial
    from typing import Optional
except ImportError:
    print("Ошибка: Не удалось импортировать модуль 'serial'")
    print("Установите его с помощью команды: pip install pyserial")
    serial = None


class ArduinoController:
    def __init__(self):
        if serial is None:
            raise ImportError(
                "Модуль 'serial' не установлен. Установите его с помощью команды: pip install pyserial")
        self.serial: Optional[serial.Serial] = None
        self.is_connected = False

    def connect(self, port: str) -> bool:
        """Подключение к Arduino"""
        try:
            self.serial = serial.Serial(port, 9600, timeout=1)
            self.is_connected = True
            return True
        except serial.SerialException as e:
            self.is_connected = False
            return False

    def disconnect(self):
        """Отключение от Arduino"""
        if self.serial and self.serial.is_open:
            self.serial.close()
        self.is_connected = False

    def press_key(self, key: str):
        """Отправка команды нажатия клавиши"""
        if self.is_connected:
            command = f"PRESS {key}\n"
            self.serial.write(command.encode())

    def release_key(self, key: str):
        """Отправка команды отпускания клавиши"""
        if self.is_connected:
            command = f"RELEASE {key}\n"
            self.serial.write(command.encode())

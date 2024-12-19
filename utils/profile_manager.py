from dataclasses import dataclass
from typing import List, Optional


@dataclass
class KeyConfig:
    key: str
    min_delay: int
    max_delay: int


@dataclass
class Profile:
    name: str
    window_title: str
    arduino_port: str
    input_method: str
    keys: List[KeyConfig]
    start_hotkey: dict
    stop_hotkey: dict


class ProfileManager:
    def __init__(self, config):
        self.config = config
        self.current_profile: Optional[Profile] = None

    def load_last_profile(self):
        """Загрузка последнего использованного профиля"""
        last_profile = self.config.get_last_profile()
        if last_profile:
            try:
                self.load_profile(last_profile)
            except Exception as e:
                print(f"Ошибка загрузки последнего профиля: {e}")

    def load_profile(self, profile_name: str) -> bool:
        """Загрузка профиля по имени"""
        config_data = self.config.load_profile(profile_name)
        if config_data:
            try:
                # Проверяем наличие всех необходимых полей
                required_fields = ['name', 'window_title', 'input_method',
                                   'arduino_port', 'keys', 'start_hotkey', 'stop_hotkey']
                if not all(field in config_data for field in required_fields):
                    raise KeyError("Отсутствуют обязательные поля в профиле")

                keys = [
                    KeyConfig(
                        key=k["key"],
                        min_delay=k["min_delay"],
                        max_delay=k["max_delay"]
                    ) for k in config_data["keys"]
                ]

                self.current_profile = Profile(
                    name=profile_name,
                    window_title=config_data["window_title"],
                    arduino_port=config_data["arduino_port"],
                    input_method=config_data["input_method"],
                    keys=keys,
                    start_hotkey=config_data["start_hotkey"],
                    stop_hotkey=config_data["stop_hotkey"]
                )
                return True
            except (KeyError, TypeError) as e:
                print(f"Ошибка загрузки профиля: {e}")
                return False
        return False

    def save_profile(self, profile):
        """Сохранение профиля"""
        # Создаем новый профиль
        new_profile = {
            "name": profile['name'],
            "window_title": profile['window_title'],
            "input_method": profile['input_method'],
            "arduino_port": profile['arduino_port'],
            "keys": [{
                "key": key['key'],
                "min_delay": key['min_delay'],
                "max_delay": key['max_delay']
            } for key in profile['keys']],
            "start_hotkey": {
                "key": profile['start_hotkey']['key'],
                "ctrl": profile['start_hotkey']['ctrl'],
                "alt": profile['start_hotkey']['alt']
            },
            "stop_hotkey": {
                "key": profile['stop_hotkey']['key'],
                "ctrl": profile['stop_hotkey']['ctrl'],
                "alt": profile['stop_hotkey']['alt']
            }
        }

        # Сохраняем профиль в конфигурацию
        self.config.save_profile(new_profile)
        self.current_profile = new_profile

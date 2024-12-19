from pathlib import Path
import json
from typing import Optional, List


class Config:
    def __init__(self):
        self.config_dir = Path('profiles')
        self.config_dir.mkdir(exist_ok=True)
        self.current_config = {}

    def save_profile(self, profile_data: dict):
        """Сохранение профиля в файл"""
        # Используем только имя профиля для создания файла
        profile_name = profile_data['name']
        file_path = self.config_dir / f"{profile_name}.json"

        # Сохраняем весь словарь профиля
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, indent=4, ensure_ascii=False)

        self.current_config = profile_data

    def load_profile(self, profile_name: str) -> Optional[dict]:
        """Загрузка профиля из файла"""
        file_path = self.config_dir / f"{profile_name}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def get_profiles_list(self) -> List[str]:
        """Получение списка доступных профилей"""
        return [f.stem for f in self.config_dir.glob('*.json')]

    def get_last_profile(self) -> Optional[str]:
        """Получение имени последнего использованного профиля"""
        profiles = self.get_profiles_list()
        if profiles:
            return profiles[0]
        return None

    def delete_profile(self, profile_name: str):
        """Удаление профиля"""
        file_path = self.config_dir / f"{profile_name}.json"
        if file_path.exists():
            file_path.unlink()

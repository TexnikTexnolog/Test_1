import win32gui
import win32con
from typing import List, Tuple, Optional


class WindowCapture:
    @staticmethod
    def get_window_list() -> List[Tuple[str, int]]:
        """Получение списка всех окон"""
        windows = []

        def enum_windows_callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    windows.append((title, hwnd))

        win32gui.EnumWindows(enum_windows_callback, None)
        return windows

    @staticmethod
    def get_window_handle(title: str) -> Optional[int]:
        """Получение handle окна по заголовку"""
        try:
            return win32gui.FindWindow(None, title)
        except win32gui.error:
            return None

    @staticmethod
    def is_window_focused(hwnd: int) -> bool:
        """Проверка, находится ли окно в фокусе"""
        return hwnd == win32gui.GetForegroundWindow()

    @staticmethod
    def set_window_focus(hwnd: int) -> bool:
        """Уст��новка фокуса на окно"""
        try:
            if win32gui.IsIconic(hwnd):  # если окно свернуто
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return True
        except win32gui.error:
            return False

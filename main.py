from gui.main_window import MainWindow
from utils.profile_manager import ProfileManager
from utils.config import Config
from PyQt5.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    config = Config()
    profile_manager = ProfileManager(config)
    window = MainWindow(profile_manager)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

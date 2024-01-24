import sys
from PySide6.QtWidgets import QApplication
from src.simulator import Simulator
from src.settings import Settings

def main():
    """A"""
    app = QApplication(sys.argv)
    Settings.screen_resolution = app.primaryScreen().size()
    sim = Simulator()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

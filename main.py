import sys
from PyQt6.QtWidgets import QApplication
from src.simulator import Simulator

def main():
    """A"""
    app = QApplication(sys.argv)
    sim = Simulator()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

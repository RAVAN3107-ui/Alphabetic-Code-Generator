import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow


def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Alphabetic Code Generator")
    window = MainWindow()
    window.show()
    return app.exec()

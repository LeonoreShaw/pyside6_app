"""Entry point for PythonStd - CSV Std Calculator."""

import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from ui.main_window import MainWindow

# main.py is the entry point for the application. It sets up the QApplication, loads assets, and shows the main window.


def get_asset_path(filename: str) -> str:
    """Get the absolute path to an asset file, works for dev and PyInstaller."""
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets", filename)


def main():
    # High DPI support
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    app = QApplication(sys.argv)
    app.setApplicationName("PythonStd")
    app.setApplicationVersion("1.0.0")

    # Set app icon
    icon_path = get_asset_path("svg.svg")
    if os.path.isfile(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Create and show main window
    window = MainWindow()
    window.show()

    # Center on screen
    screen_geo = app.primaryScreen().availableGeometry()
    window_geo = window.frameGeometry()
    center = screen_geo.center()
    window_geo.moveCenter(center)
    window.move(window_geo.topLeft())

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

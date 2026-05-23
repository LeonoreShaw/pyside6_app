@echo off
echo Building PythonStd (PySide6)...
pyinstaller --noconfirm --onefile --windowed --icon assets/icon.ico --add-data "assets;assets" main.py
echo Build complete!

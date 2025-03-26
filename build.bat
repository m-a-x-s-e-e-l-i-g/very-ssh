@echo off
echo Building SSH Launcher...

:: Clean up previous build
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
del ssh-launcher.spec >nul 2>&1

:: Run PyInstaller build
pyinstaller --onefile --noconsole launcher.py --name ssh-launcher --collect-submodules ssh_launcher

echo.
echo Build complete! Find your exe in /dist/
pause
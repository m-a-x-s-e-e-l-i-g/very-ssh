@echo off
echo Building SSH Launcher...

:: Clean up previous build
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
del ssh-launcher.spec >nul 2>&1

:: Run PyInstaller build
pyinstaller --onefile --noconsole launcher.py --name VerySSH --collect-submodules ssh_launcher --add-data "ssh_launcher/assets/icon.ico;ssh_launcher/assets" --icon "ssh_launcher/assets/icon.ico" 

echo.
echo Build complete! 
echo Find your exe in /dist/
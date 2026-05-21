@echo off
setlocal

set "MODE=%~1"
if /I "%MODE%"=="onefile" (
	set "BUILD_FLAG=--onefile"
	set "OUTPUT_HINT=dist\\VerySSH.exe"
	set "MODE_LABEL=onefile"
) else (
	set "BUILD_FLAG=--onedir"
	set "OUTPUT_HINT=dist\\VerySSH\\VerySSH.exe"
	set "MODE_LABEL=onedir (fast launch)"
)

echo Building SSH Launcher...
echo Build mode: %MODE_LABEL%

:: Clean up previous build
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
del VerySSH.spec >nul 2>&1

:: Run PyInstaller build
python -m PyInstaller %BUILD_FLAG% --noconsole launcher.py --name VerySSH --collect-submodules ssh_launcher --add-data "ssh_launcher/assets/icon.ico;ssh_launcher/assets" --icon "ssh_launcher/assets/icon.ico"

echo.
echo Build complete! 
echo Find your executable in: %OUTPUT_HINT%

if /I not "%MODE%"=="onefile" (
	echo Tip: run "build.bat onefile" if you need a single-file executable.
)
@echo off
setlocal EnableDelayedExpansion

:: Requirements
::
:: - Python 3.8.6 preferred

echo info: checking for an internet connection
ping 1.1.1.1 > nul 2>&1
if not !errorlevel! == 0 (
    echo error: no internet connection
    echo info: press any key to continue
    pause > nul 2>&1
    exit /b 1
)

set "err=0"
for %%a in (
    "python.exe"
    "pip.exe"
) do (
    where %%~a > nul 2>&1
    if not !errorlevel! == 0 (
        set "err=1"
        echo error: %%~a not found in path
    )
)
if not !err! == 0 exit /b 1

set "CURRENT_DIR=%~dp0"
set "CURRENT_DIR=!CURRENT_DIR:~0,-1!"

set "BUILD_ENV=!CURRENT_DIR!\BUILD_ENV"
set "PROJECT_DIR=!BUILD_ENV!\main"

if exist "!BUILD_ENV!" (
    rd /s /q "!BUILD_ENV!"
)
mkdir "!BUILD_ENV!"
mkdir "!PROJECT_DIR!"

python -m venv "!BUILD_ENV!"
call "!BUILD_ENV!\Scripts\activate.bat"

pip install -r "requirements.txt"

copy /y "!CURRENT_DIR!\win-wallpaper.py" "!PROJECT_DIR!"
cd "!PROJECT_DIR!"

pyinstaller "win-wallpaper.py" --onefile

call "!BUILD_ENV!\Scripts\deactivate.bat"

cd "!CURRENT_DIR!"

if exist "win-wallpaper.exe" (
    del /f /q "win-wallpaper.exe"
)

move "!PROJECT_DIR!\dist\win-wallpaper.exe" "!CURRENT_DIR!"

rd /s /q "!BUILD_ENV!"

exit /b 0

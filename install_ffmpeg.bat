@echo off
echo Installing FFmpeg for high-quality video downloads...
echo.

REM Check if winget is available (Windows 10/11)
where winget >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Using winget to install FFmpeg...
    winget install --id=Gyan.FFmpeg -e
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo FFmpeg installed successfully!
        echo Please restart your Flask app for changes to take effect.
        pause
        exit /b 0
    )
)

REM Check if chocolatey is available
where choco >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Using Chocolatey to install FFmpeg...
    choco install ffmpeg -y
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo FFmpeg installed successfully!
        echo Please restart your Flask app for changes to take effect.
        pause
        exit /b 0
    )
)

echo.
echo Automatic installation failed. Please install FFmpeg manually:
echo.
echo Option 1: Download from https://www.gyan.dev/ffmpeg/builds/
echo           Extract and add to PATH
echo.
echo Option 2: Use winget: winget install --id=Gyan.FFmpeg -e
echo.
echo Option 3: Use Chocolatey: choco install ffmpeg -y
echo.
pause

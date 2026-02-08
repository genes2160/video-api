@echo off
echo ===========================================
echo Video Processing API - Quick Start
echo ===========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)
echo [OK] Python found

:: Check FFmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] FFmpeg is not installed
    echo.
    echo Install FFmpeg:
    echo   choco install ffmpeg
    echo   OR download from https://ffmpeg.org/download.html
    pause
    exit /b 1
)
echo [OK] FFmpeg found

:: Create virtual environment
if not exist venv (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

:: Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo.
echo Installing dependencies...
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo [OK] Dependencies installed

:: Create directories
if not exist uploads mkdir uploads
if not exist outputs mkdir outputs
echo [OK] Directories created

:: Run the API
echo.
echo ===========================================
echo Starting Video Processing API...
echo ===========================================
echo.
echo API will be available at:
echo   - API:     http://localhost:8000
echo   - Swagger: http://localhost:8000/docs
echo   - ReDoc:   http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

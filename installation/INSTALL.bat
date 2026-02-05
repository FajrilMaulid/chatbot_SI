@echo off
REM Chatbot SI - Quick Setup for Windows
REM This script will:
REM - Check Python installation
REM - Install dependencies
REM - Setup database
REM - Run migration
REM - Start the application

echo ============================================================
echo    Chatbot SI - Automated Setup for Windows
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from: https://python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if MySQL is running
echo Checking MySQL...
sc query MySQL >nul 2>&1
if errorlevel 1 (
    echo [WARN] MySQL service not detected
    echo Please ensure MySQL is installed and running
    echo.
) else (
    echo [OK] MySQL service detected
    echo.
)

REM Run the main setup script
echo Running setup.py...
echo.
python setup.py

if errorlevel 1 (
    echo.
    echo [ERROR] Setup failed!
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ============================================================
echo    Setup Complete!
echo ============================================================
echo.
echo Would you like to start the application now? (Y/N)
set /p choice=

if /i "%choice%"=="Y" (
    echo.
    echo Starting application...
    python app.py
) else (
    echo.
    echo To start the application later, run: python app.py
    echo.
)

pause

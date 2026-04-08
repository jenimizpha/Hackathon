@echo off
echo ========================================
echo  Battery-Life Lab Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Check if we're in the right directory
if not exist "main.py" (
    echo ❌ Error: main.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

echo ✅ Project files found
echo.

REM Create virtual environment
echo 🐍 Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Setup completed successfully!
echo ========================================
echo.
echo To run the backend server:
echo   1. Activate the virtual environment: venv\Scripts\activate
echo   2. Run the server: python run_backend.py
echo.
echo To run the frontend:
echo   1. Open index.html in your browser, or
echo   2. Run: python -m http.server 3000
echo.
echo API Documentation: http://localhost:8000/docs
echo.
pause
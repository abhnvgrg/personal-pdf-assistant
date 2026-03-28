@echo off
REM Quick Start Script for RAG PDF Assistant
echo =====================================
echo RAG PDF Assistant - Quick Start
echo =====================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo =====================================
echo Installation complete!
echo =====================================
echo.
echo To run the application:
echo   1. Backend: python main.py
echo   2. Frontend: streamlit run app.py
echo.
echo Press any key to exit...
pause > nul

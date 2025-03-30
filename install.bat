@echo off
echo Social Media Sentiment Analysis Tool - Installation
echo ======================================================
echo.

:: Check Python version
echo Checking Python version...
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo Python not found. Please install Python 3.7 or higher.
    exit /b 1
)

:: Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment. Please install venv module.
    exit /b 1
)
echo Virtual environment created successfully.

:: Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate
echo Virtual environment activated.

:: Install dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed successfully.

:: Create .env file from example if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file from example...
    copy .env.example .env
    echo .env file created. Please edit it to add your LinkedIn credentials.
)

:: Install the package in development mode
echo.
echo Installing package in development mode...
pip install -e .
echo Package installed in development mode.

echo.
echo Installation complete!
echo.
echo To use the tool, follow these steps:
echo 1. Edit the .env file to add your LinkedIn credentials
echo 2. Activate the virtual environment with 'venv\Scripts\activate'
echo 3. Run the tool with 'python src/main.py --company "Company Name"'
echo.
echo For a quick test with mock data (no LinkedIn credentials needed):
echo python src/main.py --company "Example Corp" --use-mock-data
echo.

pause 
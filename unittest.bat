@echo off
REM Run pytest tests with coverage reporting for the visitor-management project.
cd /d "%~dp0"

set "VENV_PY=%~dp0venv\Scripts\python.exe"
if exist "%VENV_PY%" (
    echo Checking virtual environment Python at "%VENV_PY%"
    call "%VENV_PY%" -c "import sys" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo Running tests with coverage
        call "%VENV_PY%" -m pytest --cov=src --cov-report term-missing --cov-report html:coverage_html tests
        exit /b %ERRORLEVEL%
    ) else (
        echo Virtual environment Python exists but is not valid.
    )
)

echo Could not run tests with the repo virtual environment.
echo Please recreate the virtual environment using:
	echo   python -m venv venv
	echo   venv\Scripts\activate
	echo   python -m pip install -r requirements.txt
exit /b 1

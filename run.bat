@echo off
cd /d "%~dp0"

echo ========================================
echo   Markdown to PDF
echo ========================================
echo.

:: find Python
set PY=
py --version >nul 2>&1
if %errorlevel% equ 0 set PY=py
if "%PY%"=="" (
    python --version >nul 2>&1
    if %errorlevel% equ 0 set PY=python
)
if "%PY%"=="" (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 set PY=python3
)

if "%PY%"=="" (
    echo [X] Python not found.
    echo Please install Python 3.8+
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python: %PY%
echo.

:: install deps
echo [1/2] Checking dependencies...
%PY% -c "import markdown" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing...
    %PY% -m pip install -r requirements.txt -q
    if %errorlevel% neq 0 (
        echo [X] Install failed. Check your network.
        pause
        exit /b 1
    )
)
echo Done.
echo.

:: convert
echo [2/2] Converting...
echo.
%PY% md2pdf.py

echo.
echo ========================================
pause

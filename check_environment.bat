@echo off
echo JavaScript to Python Converter - Environment Check
echo ==============================================
echo.

echo Checking for required software...
echo.

echo 1. Checking for Python...
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python --version
    echo Python is installed and available.
    echo.
) else (
    echo Python is NOT installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
)

echo 2. Checking for PHP...
where php >nul 2>nul
if %ERRORLEVEL% equ 0 (
    php -v | findstr /R "^PHP"
    echo PHP is installed and available.
    echo.
) else (
    echo PHP is NOT installed or not in your PATH.
    echo This is optional but recommended for the web interface.
    echo You can install PHP from https://windows.php.net/download/
    echo.
)

echo 3. Checking for C++ converter...
if exist final_js2py.exe (
    echo C++ converter (final_js2py.exe) is available.
    echo.
) else (
    echo C++ converter (final_js2py.exe) is NOT found.
    echo This is one of the converter options.
    echo.
)

echo 4. Checking for Python converters...
if exist js2py_converter.py (
    echo Python converter (js2py_converter.py) is available.
    echo.
) else (
    echo Python converter (js2py_converter.py) is NOT found.
    echo This is one of the converter options.
    echo.
)

if exist js2py_improved.py (
    echo Improved Python converter (js2py_improved.py) is available.
    echo.
) else (
    echo Improved Python converter (js2py_improved.py) is NOT found.
    echo This is one of the converter options.
    echo.
)

echo 5. Checking for web interface files...
if exist index.html (
    echo Web interface (index.html) is available.
    echo.
) else (
    echo Web interface (index.html) is NOT found.
    echo This is needed for the web interface.
    echo.
)

echo Environment check complete.
echo.
echo If any components are missing, please refer to the README.md and TROUBLESHOOTING.md files.
echo.
pause
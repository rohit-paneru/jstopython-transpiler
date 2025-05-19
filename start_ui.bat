@echo off
echo Starting JavaScript to Python Converter UI...
echo.
echo Please wait while the server starts...
echo.
echo Once the server is running, open your web browser and go to:
echo http://localhost:8000
echo.
echo Press Ctrl+C to stop the server when you're done.
echo.
python server.py

REM If the server exits, show a message
echo.
echo Server stopped.
pause
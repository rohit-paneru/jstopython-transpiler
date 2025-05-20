@echo off
title JSTOP Transpiler Server
echo Starting JSTOP Web UI (Python Flask Server)...
echo.
echo The Flask server will attempt to run on http://127.0.0.1:5000/
echo (or http://YOUR_LOCAL_IP:5000/ if accessed from another device on network).
echo Open this address in your web browser once the server messages appear.
echo.
echo Press CTRL+C in this window to stop the server.
echo.

python server.py

echo.
echo Flask server has been stopped.
pause
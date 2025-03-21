@echo off
echo Starting Flask/Dash app with Waitress...
cd /d "%~dp0"
start "" cmd /k "py -m waitress --listen=127.0.0.1:5000 app:server"
timeout /t 5 >nul
start "" http://127.0.0.1:5000/
exit 	
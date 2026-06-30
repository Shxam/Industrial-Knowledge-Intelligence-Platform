@echo off
echo ================================================
echo   Starting IKIP Development Environment
echo ================================================
echo.

REM Start Backend in new window
echo [1/2] Starting Backend Server...
start "IKIP Backend" cmd /k "cd backend && venv\Scripts\activate && echo Backend Starting... && uvicorn simple_server:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak > nul

REM Start Frontend in new window
echo [2/2] Starting Frontend Server...
start "IKIP Frontend" cmd /k "cd frontend && echo Frontend Starting... && npm run dev"

echo.
echo ================================================
echo   Services Starting...
echo ================================================
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:5173
echo API Docs will be available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C in each terminal window to stop services
echo.
pause

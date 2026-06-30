@echo off
REM Quick start script for IKIP on Windows

echo =========================================
echo   IKIP (Pragya) - Quick Start
echo =========================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo [1/4] Creating .env file...
    copy .env.example .env
    echo.
    echo WARNING: Please edit .env and add your API keys!
    echo.
    pause
) else (
    echo [1/4] .env file exists
)

REM Create data directories
echo [2/4] Creating directories...
if not exist "data\faiss_index" mkdir data\faiss_index
if not exist "data\uploads" mkdir data\uploads
if not exist "data\processed" mkdir data\processed
if not exist "backend\logs" mkdir backend\logs

REM Start Docker services
echo [3/4] Starting Docker services...
docker-compose up -d
echo.
echo Waiting for services to start...
timeout /t 10 /nobreak > nul

REM Show service status
echo [4/4] Checking service status...
docker-compose ps
echo.

echo =========================================
echo   Setup Complete!
echo =========================================
echo.
echo Next steps:
echo.
echo 1. Setup Backend:
echo    cd backend
echo    python -m venv venv
echo    venv\Scripts\activate
echo    pip install -r requirements.txt
echo.
echo 2. Start Backend:
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn app.main:app --reload
echo.
echo 3. Access Services:
echo    - API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo    - Neo4j: http://localhost:7474
echo    - MinIO: http://localhost:9001
echo.
pause

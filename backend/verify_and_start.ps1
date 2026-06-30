# Backend Verification and Startup Script
# ET-Hackathon - IKIP Project

Write-Host "`n=== IKIP Backend Verification & Startup ===" -ForegroundColor Cyan
Write-Host "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n" -ForegroundColor Gray

# Step 1: Check Python Version
Write-Host "[1/7] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "  ✓ $pythonVersion" -ForegroundColor Green

# Step 2: Verify Virtual Environment
Write-Host "`n[2/7] Verifying virtual environment..." -ForegroundColor Yellow
if (Test-Path ".\venv") {
    Write-Host "  ✓ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "  ✗ Virtual environment not found!" -ForegroundColor Red
    Write-Host "  Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}

# Step 3: Check Critical Packages
Write-Host "`n[3/7] Checking critical packages..." -ForegroundColor Yellow
.\venv\Scripts\python.exe -m pip list | Select-String -Pattern "spacy|neo4j|torch|fastapi" | ForEach-Object {
    Write-Host "  ✓ $_" -ForegroundColor Green
}

# Step 4: Verify Configuration
Write-Host "`n[4/7] Verifying configuration..." -ForegroundColor Yellow
$config = .\venv\Scripts\python.exe -c "import sys; sys.path.insert(0, '.'); from app.core.config import settings; print(f'Provider:{settings.LLM_PROVIDER}|Model:{settings.LLM_MODEL}|GROQ:{bool(settings.GROQ_API_KEY)}')"
$configParts = $config -split '\|'
Write-Host "  ✓ LLM Provider: $($configParts[0] -replace 'Provider:','')" -ForegroundColor Green
Write-Host "  ✓ LLM Model: $($configParts[1] -replace 'Model:','')" -ForegroundColor Green
Write-Host "  ✓ GROQ API Key: $($configParts[2] -replace 'GROQ:','')" -ForegroundColor Green

# Step 5: Check Docker Services
Write-Host "`n[5/7] Checking Docker services..." -ForegroundColor Yellow
Set-Location ..
$services = docker-compose ps --services 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Docker Compose not available or no services running" -ForegroundColor Red
    Write-Host "  Run 'docker-compose up -d' to start services" -ForegroundColor Yellow
} else {
    $runningServices = docker-compose ps --filter "status=running" --services
    if ($runningServices) {
        Write-Host "  ✓ Running services:" -ForegroundColor Green
        $runningServices | ForEach-Object { Write-Host "    - $_" -ForegroundColor Cyan }
    } else {
        Write-Host "  ⚠ No services running" -ForegroundColor Yellow
        Write-Host "  Starting services with docker-compose..." -ForegroundColor Yellow
        docker-compose up -d
        Start-Sleep -Seconds 5
        Write-Host "  ✓ Services started" -ForegroundColor Green
    }
}
Set-Location backend

# Step 6: Test Module Imports
Write-Host "`n[6/7] Testing module imports..." -ForegroundColor Yellow
$importTest = .\venv\Scripts\python.exe -c "import sys; sys.path.insert(0, '.'); from app.core.config import settings; from app.core.logging import logger; print('OK')" 2>&1
if ($importTest -match "OK") {
    Write-Host "  ✓ Core modules import successfully" -ForegroundColor Green
} else {
    Write-Host "  ✗ Import errors detected" -ForegroundColor Red
    Write-Host $importTest
}

# Step 7: Display Next Steps
Write-Host "`n[7/7] Verification Complete!" -ForegroundColor Green
Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Ensure Docker services are running:" -ForegroundColor White
Write-Host "   docker-compose ps" -ForegroundColor Gray
Write-Host "`n2. Start the backend server:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\activate" -ForegroundColor Gray
Write-Host "   python app/main.py" -ForegroundColor Gray
Write-Host "`n   OR" -ForegroundColor Yellow
Write-Host "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor Gray
Write-Host "`n3. Access the API documentation:" -ForegroundColor White
Write-Host "   http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`n4. Test the health endpoint:" -ForegroundColor White
Write-Host "   curl http://localhost:8000/api/v1/health" -ForegroundColor Gray
Write-Host "`n=== Services Access ===" -ForegroundColor Cyan
Write-Host "  Neo4j Browser:  http://localhost:7474 (neo4j/neo4j_password_change_me)" -ForegroundColor Gray
Write-Host "  MinIO Console:  http://localhost:9001 (minioadmin/minioadmin)" -ForegroundColor Gray
Write-Host "  API Docs:       http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "`n" -ForegroundColor White

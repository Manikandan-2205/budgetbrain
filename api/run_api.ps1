Write-Host "Starting BudgetBrain API Server..." -ForegroundColor Green
Set-Location $PSScriptRoot
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
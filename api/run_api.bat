@echo off
echo Starting BudgetBrain API Server...
cd /d %~dp0
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
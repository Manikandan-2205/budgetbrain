Write-Host "Starting BudgetBrain UI..." -ForegroundColor Green
Set-Location $PSScriptRoot
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
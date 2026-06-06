<#
PowerShell helper: run the Streamlit app
Usage:
  Copy .env.example to .env and fill keys.
  Activate venv: .\.venv\Scripts\Activate.ps1
  Run: .\scripts\run.ps1
#>
if (-Not (Test-Path './.venv')) {
    Write-Host "Virtual environment not found. Run scripts/install.ps1 first." -ForegroundColor Yellow
    exit 1
}
& ".\.venv\Scripts\Activate.ps1"
py -m streamlit run app.py

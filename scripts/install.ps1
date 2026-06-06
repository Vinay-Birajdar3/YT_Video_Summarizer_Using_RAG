<#
PowerShell helper: create virtual environment and install requirements
Usage: Open PowerShell in the repo root and run:
  .\scripts\install.ps1
#>
$venv = "./.venv"
if (-Not (Test-Path $venv)) {
    python -m venv $venv
}
& "$venv/Scripts/Activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Write-Host "Dependencies installed. Activate with `.$venv/Scripts/Activate.ps1` and run the app with scripts/run.ps1"

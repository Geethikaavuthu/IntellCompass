# setup_dev.ps1
# Create a virtual environment and install minimal requirements quickly (no cache).
# Run from repository root (PowerShell): .\scripts\setup_dev.ps1

$venvPath = ".\.venv"
$requirements = ".\INTELLICOMPASS\requirements-minimal.txt"

Write-Host "Creating virtual environment at $venvPath..." -ForegroundColor Cyan
if (-Not (Test-Path $venvPath)) {
    python -m venv $venvPath
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
}

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& "$venvPath\Scripts\Activate.ps1"

Write-Host "Upgrading pip and installing minimal requirements (no cache)..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r $requirements

Write-Host "Setup complete." -ForegroundColor Green
Write-Host "To run the server:" -ForegroundColor Cyan
Write-Host "  .\\.venv\\Scripts\\Activate.ps1" -ForegroundColor Magenta
Write-Host "  python INTELLICOMPASS/manage.py runserver" -ForegroundColor Magenta

Write-Host "If you want to enable SMTP mail, run scripts/setup_mail.ps1 and edit INTELLICOMPASS/.env" -ForegroundColor Cyan

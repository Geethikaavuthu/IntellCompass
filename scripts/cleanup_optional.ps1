# cleanup_optional.ps1
# Uninstall optional heavy packages to free disk space.
# Usage: .\scripts\cleanup_optional.ps1

$venvPath = ".\.venv"
if (-Not (Test-Path $venvPath)) {
    Write-Host ".venv not found. If you installed packages globally, run this script from the environment where they were installed." -ForegroundColor Yellow
}

Write-Host "Activating virtual environment (if present)..." -ForegroundColor Cyan
if (Test-Path $venvPath) { & "$venvPath\Scripts\Activate.ps1" }

Write-Host "Uninstalling optional heavy packages..." -ForegroundColor Cyan
python -m pip uninstall -y google-generativeai grpcio protobuf google-api-core google-api-python-client

Write-Host "Cleanup complete. Consider running: python -m pip cache purge" -ForegroundColor Green

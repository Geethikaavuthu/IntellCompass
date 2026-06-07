# test_mail.ps1
# Activates venv and sends a test email via Django send_mail (uses EMAIL settings from .env)
# Usage: run from repository root: .\scripts\test_mail.ps1 "you@domain.com"

param(
    [string]$To = "geethikareddy.avuthu@gmail.com"
)

$venvPath = ".\.venv"
if (-Not (Test-Path $venvPath)) {
    Write-Host ".venv not found. Run scripts/setup_dev.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& "$venvPath\Scripts\Activate.ps1"

Write-Host "Sending test email to $To..." -ForegroundColor Cyan
$cmd = "python INTELLICOMPASS/manage.py shell -c \"from django.core.mail import send_mail; send_mail('IntelliCompass test','This is a test email','no-reply@intellicompass.local',['$To'],fail_silently=False)\""
Invoke-Expression $cmd

Write-Host "Test email command complete. Check console output or recipient inbox." -ForegroundColor Green

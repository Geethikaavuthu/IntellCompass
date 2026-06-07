# setup_mail.ps1
# Copies the mail example env to .env for local editing and reminds you to update secrets.
# Usage: run from repository root (PowerShell): .\scripts\setup_mail.ps1

$src = "." + "\INTELLICOMPASS\.env.mail.example"
$dst = "." + "\INTELLICOMPASS\.env"

if (Test-Path $dst) {
    Write-Host ".env already exists at $dst. Backing up to .env.bak" -ForegroundColor Yellow
    Copy-Item $dst "$dst.bak" -Force
}

Copy-Item $src $dst -Force
Write-Host "Created/updated .env from .env.mail.example at $dst" -ForegroundColor Green
Write-Host "Edit the file and fill in your SMTP credentials, then restart the Django server." -ForegroundColor Cyan
Write-Host "To test sending a mail from the Django shell run:" -ForegroundColor Cyan
Write-Host "  python manage.py shell -c \"from django.core.mail import send_mail; send_mail('Test','Body','from@example.com',['you@domain.com'],fail_silently=False)\"" -ForegroundColor Magenta

Mail authentication setup (no code changes)
===========================================

This project already reads environment variables via python-dotenv (see `intellicompass/settings.py`), so you can enable SMTP mail sending without modifying code. Follow these steps:

1. Copy the example env file and edit secrets
   - Copy `.env.mail.example` to `.env` (script provided):
     - PowerShell (from repo root):
       ```powershell
       .\scripts\setup_mail.ps1
       ```
     - Or copy manually: create `INTELLICOMPASS/INTELLICOMPASS/.env` and paste values.

2. Fill in your SMTP provider values in `.env`:
   - `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
   - `EMAIL_HOST`, `EMAIL_PORT`
   - `EMAIL_USE_TLS` or `EMAIL_USE_SSL`
   - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
   - `DEFAULT_FROM_EMAIL`

3. (Optional but recommended) Configure Redis for cache if running multiple processes. Set `REDIS_URL` in `.env` (example provided in `.env.mail.example`).

4. Restart the Django development server to pick up `.env` changes.

Testing email sending
---------------------
- Quick test via Django shell:
```powershell
python manage.py shell -c "from django.core.mail import send_mail; send_mail('Test','Body','from@example.com',['you@domain.com'],fail_silently=False)"
```
- Or register a new user and confirm you receive the OTP email.

Security notes
--------------
- Do NOT commit `.env` to source control; keep it secret.
- Use provider API keys and rotate them periodically.
- For Gmail, create an App Password and enable 2FA instead of using your account password.

If you want, I can also:
- Add a tiny script to run the test mail command automatically.
- Add a GitHub Action that validates SMTP settings (without leaking secrets) in a secure way.

Files added
- `.env.mail.example` — example SMTP env values (INTELLICOMPASS/INTELLICOMPASS/.env.mail.example)
- `scripts/setup_mail.ps1` — helper to copy example to `.env`
- `README_MAIL.md` — concise setup and test instructions (INTELLICOMPASS/INTELLICOMPASS/README_MAIL.md)

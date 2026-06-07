#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path
from firebase_admin import auth, credentials, initialize_app

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


if load_dotenv:
    load_dotenv(Path("INTELLICOMPASS/.env"))


def load_token(argv):
    if len(argv) > 1 and argv[1] and not argv[1].startswith("<"):
        return argv[1]

    env_token = os.getenv("FIREBASE_TEST_IDTOKEN", "").strip()
    if env_token:
        return env_token

    token_file = Path("scripts/idtoken.txt")
    if token_file.exists():
        token = token_file.read_text(encoding="utf-8").strip()
        if token:
            return token

    return None


cred_path = os.getenv('FIREBASE_CREDENTIALS', '').strip()
if not cred_path:
    print('Set FIREBASE_CREDENTIALS env var to service account JSON path.')
    sys.exit(1)

if not Path(cred_path).exists():
    print(f'FIREBASE_CREDENTIALS path does not exist: {cred_path}')
    sys.exit(1)

with open(cred_path, 'r', encoding='utf-8-sig') as cred_file:
    cred_data = json.load(cred_file)

cred = credentials.Certificate(cred_data)
initialize_app(cred)

token = load_token(sys.argv)
if not token:
    print('Usage: python verify_firebase_token.py <idToken>')
    print('Or set FIREBASE_TEST_IDTOKEN in .env or create scripts/idtoken.txt')
    sys.exit(2)

try:
    decoded = auth.verify_id_token(token)
    print('Token valid. Decoded payload:')
    print(decoded)
except Exception as e:
    print('Token verification failed:', e)
    sys.exit(3)

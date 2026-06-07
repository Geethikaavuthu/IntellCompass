import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Ensure the inner project package (INTELLICOMPASS/INTELLICOMPASS) is importable
sys.path.insert(0, os.path.join(project_root, 'INTELLICOMPASS'))
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intellicompass.settings')
import django
django.setup()
from django.test import Client
c = Client()
resp = c.get('/')
print('STATUS:', resp.status_code)
content = resp.content.decode('utf-8', errors='replace')
print(content[:8000])

from django.conf import settings
import json

def firebase_config(request):
    """Provide FIREBASE_CLIENT_CONFIG to templates as a JS object or empty string."""
    cfg = getattr(settings, 'FIREBASE_CLIENT_CONFIG_JSON', '')
    if not cfg:
        return {'FIREBASE_CLIENT_CONFIG': ''}
    try:
        # make sure it's valid JSON
        parsed = json.loads(cfg)
        return {'FIREBASE_CLIENT_CONFIG': parsed}
    except Exception:
        return {'FIREBASE_CLIENT_CONFIG': ''}

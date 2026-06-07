import os
from django.conf import settings
from django.contrib.auth import get_user_model

try:
    import firebase_admin
    from firebase_admin import auth as firebase_auth
    from firebase_admin import credentials
except Exception:
    firebase_admin = None
    firebase_auth = None

User = get_user_model()

FIREBASE_APP = None


def init_firebase_app():
    global FIREBASE_APP
    if FIREBASE_APP or not firebase_admin:
        return
    cred_path = os.getenv('FIREBASE_CREDENTIALS')
    cred_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
    try:
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            FIREBASE_APP = firebase_admin.initialize_app(cred)
        elif cred_json:
            # cred_json expected to be a JSON string
            import json
            data = json.loads(cred_json)
            cred = credentials.Certificate(data)
            FIREBASE_APP = firebase_admin.initialize_app(cred)
        else:
            # try application default
            FIREBASE_APP = firebase_admin.initialize_app()
    except Exception as e:
        FIREBASE_APP = None


class FirebaseBackend:
    """Authentication backend that accepts a Firebase ID token.

    Usage: call authenticate(request, firebase_token=token)
    """

    def authenticate(self, request, firebase_token=None):
        if not firebase_admin:
            return None
        init_firebase_app()
        if not firebase_auth:
            return None
        if not firebase_token:
            return None
        try:
            decoded = firebase_auth.verify_id_token(firebase_token)
        except Exception:
            return None
        uid = decoded.get('uid')
        email = decoded.get('email')
        if not uid:
            return None
        # Use uid as username to avoid collisions; store email
        username = f"fb_{uid}"
        user, created = User.objects.get_or_create(username=username, defaults={
            'email': email or '',
            'is_active': True,
        })
        # Ensure email is set
        if email and user.email != email:
            user.email = email
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

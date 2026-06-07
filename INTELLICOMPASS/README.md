# IntelliCompass: AI-Enhanced Personalized E-Learning Platform

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your SECRET_KEY and GEMINI_API_KEY

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (admin)
python manage.py createsuperuser

# 6. Load sample data (optional)
python manage.py seed_data

# 7. Run the server
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## Firebase Auth Setup

This project now uses Firebase Auth for client-side sign-in and sign-up.

### Firebase Console

1. Create or open your Firebase project.
2. Go to Authentication and enable the sign-in providers you want:
	- Email/Password
	- Google
	- Facebook
3. In Project settings, add your web app and copy the Firebase config values.
4. Download a service account JSON file for server-side token verification.

### Environment Variables

Add these values to your `.env` file:

```text
FIREBASE_CLIENT_CONFIG_JSON={"apiKey":"...","authDomain":"...","projectId":"...","storageBucket":"...","messagingSenderId":"...","appId":"..."}
FIREBASE_CREDENTIALS=C:/path/to/serviceAccount.json
```

Optional for local testing:

```text
FIREBASE_TEST_IDTOKEN=<paste-a-real-firebase-id-token-here>
```

### Client Flow

- Users sign in or sign up through the Firebase buttons on the login and registration pages.
- The client gets a Firebase ID token.
- The app posts that token to `/accounts/firebase-login/`.
- Django verifies the token with `firebase-admin` and creates/logs in the user session.

### Deployment Notes

- Do not commit service account JSON files or ID tokens.
- Set `DEBUG=False` in production.
- Keep `FIREBASE_CLIENT_CONFIG_JSON` public-safe only.
- Make sure the Firebase providers are enabled in the console before deploying the social sign-in buttons.

### Deployment Checklist

1. Set production environment variables for Django and Firebase.
2. Verify Firebase Google/Facebook providers are enabled in the Firebase console.
3. Point `FIREBASE_CREDENTIALS` to the service account JSON on the server.
4. Deploy Django to a Python host and Firebase Hosting only for static/client assets if needed.
5. Confirm login, social sign-in, and token verification before going live.

### Firebase Hosting

Firebase Hosting is only suitable for the client-side front end or static assets. The Django backend still needs a Python host such as Render, Cloud Run, Railway, or a VPS.

If you want to host a static front-end bundle with Firebase Hosting, copy the example files and replace the placeholders:

```bash
cp firebase.json.example firebase.json
cp .firebaserc.example .firebaserc
```

Example files included in the repo:

- `firebase.json.example`
- `.firebaserc.example`

For a full deployment, keep Django running on your Python host and point the Firebase client app at that backend endpoint.

## User Roles
- **Student**: Enroll in courses, take quizzes, track progress
- **Instructor**: Create courses/lessons, view student analytics
- **Admin**: Full platform analytics, user management, feedback monitoring

## Features
- Adaptive AI quizzes via Gemini API
- Webcam-based engagement monitoring (TensorFlow.js)
- Real-time dashboards with Chart.js
- Personalized learning recommendations
- Light/Dark mode toggle
- Responsive pastel UI with Bootstrap 5

## Project Structure
```
intellicompass/          # Django project settings
accounts/                # Authentication & user management
courses/                 # Course & lesson management
quizzes/                 # Quiz engine with Gemini integration
monitoring/              # Webcam engagement tracking
analytics/               # Dashboards & progress tracking
feedback/                # Feedback system
recommendations/         # AI-powered recommendations
templates/               # HTML templates
static/                  # CSS, JS, images
```

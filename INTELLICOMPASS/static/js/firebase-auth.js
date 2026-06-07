// Minimal Firebase Auth helper for IntelliCompass
(function(){
  function formatError(e) {
    if (!e) return 'Authentication failed.';
    if (e.code === 'auth/invalid-api-key') {
      return 'Firebase is not configured. Set FIREBASE_CLIENT_CONFIG_JSON with a valid apiKey from your Firebase web app.';
    }
    return e.message || String(e);
  }

  function ensureReady(onError) {
    const config = window.FIREBASE_CLIENT_CONFIG;
    const requiredFields = ['apiKey', 'authDomain', 'projectId', 'appId'];
    const isMissingFields = !config || typeof config !== 'object' || requiredFields.some(field => !config[field] || config[field].includes('YOUR_'));

    if (isMissingFields) {
      const msg = 'Firebase configuration is missing or contains placeholders. Please update .env with real values.';
      console.error(msg);
      if (onError) onError(msg);
      return false;
    }
    if (typeof firebase === 'undefined') {
      if (onError) onError('Firebase SDK not loaded.');
      return false;
    }
    return true;
  }

  function _init() {
    if (!ensureReady()) {
      return;
    }
    try {
      if (!firebase.apps.length) {
        firebase.initializeApp(window.FIREBASE_CLIENT_CONFIG);
      }
    } catch(e) {
      console.error('Firebase init error', e);
    }
  }

  async function postIdToken(idToken) {
    try {
      const resp = await fetch('/accounts/firebase-login/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({idToken})
      });
      return resp.json();
    } catch (e) {
      console.error('Failed to post idToken', e);
      throw e;
    }
  }

  async function registerWithEmail(email, password, onError) {
    try {
      if (!ensureReady(onError)) return;
      const cred = await firebase.auth().createUserWithEmailAndPassword(email, password);
      const idToken = await cred.user.getIdToken();
      const res = await postIdToken(idToken);
      if (res && res.status === 'ok') window.location = res.next || '/';
    } catch (e) {
      console.error(e);
      if (onError) onError(formatError(e));
    }
  }

  async function loginWithEmail(email, password, onError) {
    try {
      if (!ensureReady(onError)) return;
      const cred = await firebase.auth().signInWithEmailAndPassword(email, password);
      const idToken = await cred.user.getIdToken();
      const res = await postIdToken(idToken);
      if (res && res.status === 'ok') window.location = res.next || '/';
    } catch (e) {
      console.error(e);
      if (onError) onError(formatError(e));
    }
  }

  async function signInWithGoogle(onError) {
    try {
      if (!ensureReady(onError)) return;
      var provider = new firebase.auth.GoogleAuthProvider();
      const result = await firebase.auth().signInWithPopup(provider);
      const idToken = await result.user.getIdToken();
      const res = await postIdToken(idToken);
      if (res && res.status === 'ok') window.location = res.next || '/';
    } catch (e) {
      console.error(e);
      if (onError) onError(formatError(e));
    }
  }

  async function signInWithFacebook(onError) {
    try {
      if (!ensureReady(onError)) return;
      var provider = new firebase.auth.FacebookAuthProvider();
      const result = await firebase.auth().signInWithPopup(provider);
      const idToken = await result.user.getIdToken();
      const res = await postIdToken(idToken);
      if (res && res.status === 'ok') window.location = res.next || '/';
    } catch (e) {
      console.error(e);
      if (onError) onError(formatError(e));
    }
  }

  // expose
  window.IntellicompassFirebaseAuth = {
    init: _init,
    registerWithEmail,
    loginWithEmail
    , signInWithGoogle, signInWithFacebook
  };

  document.addEventListener('DOMContentLoaded', function(){
    _init();
  });
})();

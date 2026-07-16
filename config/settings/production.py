"""
Production settings — secure defaults. All secrets come from the environment.

Required env vars in production:
  DJANGO_ENV=production
  DJANGO_SECRET_KEY=<a long random string>
  DJANGO_DEBUG=False
  DJANGO_ALLOWED_HOSTS=augytravels.com,www.augytravels.com
"""
from .base import *  # noqa: F401,F403

DEBUG = False

# Fail loudly if the secret key was not overridden.
if SECRET_KEY.startswith("django-insecure"):  # noqa: F405
    raise RuntimeError("DJANGO_SECRET_KEY must be set to a secure value in production.")

# --- Security headers -------------------------------------------------------
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
X_FRAME_OPTIONS = "DENY"

# NOTE (Phase 2/3): add WhiteNoise for static serving and PostgreSQL here.

"""Development settings — DEBUG on, console email, local hosts."""
from .base import *  # noqa: F401,F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Emails (e.g. enquiry notifications) print to the console in dev.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

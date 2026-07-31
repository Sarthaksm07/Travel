"""Development settings — DEBUG on, console email, local hosts."""
from .base import *  # noqa: F401,F403

DEBUG = True

# In development, allow any host so the site is reachable from other devices
# on the same network (phone/tablet) via your machine's LAN IP.
ALLOWED_HOSTS = ["*"]

# Emails (e.g. enquiry notifications) print to the console in dev.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

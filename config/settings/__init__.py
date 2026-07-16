"""
Select the settings module based on the DJANGO_ENV environment variable.

    DJANGO_ENV=development  (default)  -> config/settings/development.py
    DJANGO_ENV=production              -> config/settings/production.py
"""
import os

_env = os.environ.get("DJANGO_ENV", "development").lower()

if _env == "production":
    from .production import *  # noqa: F401,F403
else:
    from .development import *  # noqa: F401,F403

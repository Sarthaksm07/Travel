"""
Base settings shared across all environments.

Environment is selected in config/settings/__init__.py via the DJANGO_ENV
environment variable ("development" by default, "production" for prod).
Secrets and environment-specific values are read from environment variables
so nothing sensitive is committed. See .env.example.
"""
import os
import sys
from pathlib import Path

# config/settings/base.py -> project root is three parents up.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Allow first-party apps to live under apps/ and be imported by short name
# (e.g. "core", "packages") instead of "apps.core".
sys.path.insert(0, str(BASE_DIR / "apps"))

# --- Core -------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-key-change-in-production",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]

# --- Applications -----------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_ckeditor_5",
]

LOCAL_APPS = [
    "core",
    "destinations",
    "tours",
    "blog",
    "testimonials",
    "leads",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Database ---------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Password validation ----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internationalization ---------------------------------------------------
LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# --- Static & media ---------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Rich text editor (CKEditor 5) -----------------------------------------
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading", "|", "bold", "italic", "link",
            "bulletedList", "numberedList", "blockQuote", "|",
            "insertImage", "|", "undo", "redo",
        ],
    },
    "extends": {
        "toolbar": [
            "heading", "|", "bold", "italic", "underline", "link",
            "bulletedList", "numberedList", "todoList", "blockQuote", "|",
            "insertImage", "mediaEmbed", "insertTable", "|", "undo", "redo",
        ],
        "image": {
            "toolbar": ["imageTextAlternative", "imageStyle:full", "imageStyle:side"],
        },
    },
}

# --- Email (enquiry notifications) -----------------------------------------
# Dev prints to console (set in development.py). Production uses SMTP via env.
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", "no-reply@augytravels.com")
LEADS_NOTIFY_EMAIL = os.environ.get("DJANGO_LEADS_NOTIFY_EMAIL", "augytravels@gmail.com")

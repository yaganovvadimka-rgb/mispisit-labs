"""Настройки первой страницы без базы данных и пользовательских сессий."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Только для учебной информационной страницы без учётных записей.
SECRET_KEY = "lab1-auto-service-registration-information-page"
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
INSTALLED_APPS = []
MIDDLEWARE = []
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": False,
    },
]
DATABASES = {}

LANGUAGE_CODE = "ru"

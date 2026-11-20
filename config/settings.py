"""Настройки приложения онлайн-записи в автосервис (версия 0.0.5).

Данные хранятся в PostgreSQL. Адрес базы, логин и пароль приходят
из переменной окружения DATABASE_URL, которую задаёт docker-compose.yml.
"""

import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Учебный проект без учётных записей: ключ нужен только для CSRF-защиты форм.
SECRET_KEY = os.environ.get("SECRET_KEY", "lab3-auto-service-booking-demo-key")
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "booking",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "booking.context_processors.app_info",
            ],
        },
    },
]

if "DATABASE_URL" not in os.environ:
    raise RuntimeError(
        "Не задана переменная DATABASE_URL. Запускайте проект через docker compose up -d")

DATABASES = {
    "default": dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=60),
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

APP_NAME = "Система онлайн-записи в автосервис"
APP_VERSION = "0.0.5"

LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Ulyanovsk"
USE_TZ = False
USE_I18N = True

"""Настройки приложения онлайн-записи в автосервис (версия 0.0.2).

База данных пока не подключается: данные хранятся в JSON-файлах папки data/.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Учебный проект без учётных записей: ключ нужен только для CSRF-защиты форм.
SECRET_KEY = "lab2-auto-service-booking-demo-key"
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

INSTALLED_APPS = [
    "booking",
]

MIDDLEWARE = [
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
            ],
        },
    },
]

# Отдельная база появится в следующей работе.
DATABASES = {}

# Папка с демо-данными (услуги, мастера, записи, журнал отказов).
DATA_DIR = Path(os.environ.get("DATA_DIR", BASE_DIR / "data"))

APP_NAME = "Система онлайн-записи в автосервис"
APP_VERSION = "0.0.2"

LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Ulyanovsk"
USE_TZ = False
USE_I18N = True

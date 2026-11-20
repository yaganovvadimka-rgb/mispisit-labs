#!/bin/sh
# Создаёт структуру базы (миграции) и запускает приложение.
# Если база ещё не принимает подключения, повторяет попытку.
set -e

attempt=1
until python manage.py migrate --noinput; do
    if [ "$attempt" -ge 30 ]; then
        echo "База данных недоступна, приложение не запущено." >&2
        exit 1
    fi
    echo "База ещё не готова, попытка $attempt из 30. Повтор через 2 секунды..."
    attempt=$((attempt + 1))
    sleep 2
done

exec python manage.py runserver 0.0.0.0:8080 --noreload

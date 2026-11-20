FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Часовой пояс нужен для проверки «нельзя записаться в прошлое».
RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY manage.py entrypoint.sh ./
COPY config/ ./config/
COPY booking/ ./booking/
COPY templates/ ./templates/

RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

EXPOSE 8080

CMD ["./entrypoint.sh"]

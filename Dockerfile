FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY manage.py ./
COPY config/ ./config/
COPY templates/ ./templates/

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080", "--noreload"]

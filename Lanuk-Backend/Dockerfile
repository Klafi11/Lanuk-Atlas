FROM python:3.12

# Setze Umgebungsvariablen
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV BACKEND_PORT=8000

# Setze Arbeitsverzeichnis
WORKDIR /app

# Installiere Systemabhängigkeiten
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Kopiere requirements zuerst (für besseres Caching)
COPY requirements.txt .

# Installiere Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Erstelle einen Nicht-Root-Benutzer für mehr Sicherheit
RUN useradd --create-home --shell /bin/bash app

# Kopiere Anwendungscode
COPY . .

# Erstelle Logs-Verzeichnis und setze Eigentümerrechte NACH dem Kopieren des Codes
RUN mkdir -p /app/logs && chown -R app:app /app

# Wechsel zu Nicht-Root-Benutzer
USER app

# Öffne Port unter Verwendung der Umgebungsvariablen
EXPOSE $BACKEND_PORT

# Verwende Umgebungsvariable im Gunicorn-Befehl
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$BACKEND_PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker --timeout 1800 --graceful-timeout 1800 --keep-alive 1800 --max-requests 1000 --max-requests-jitter 50 --backlog 2048 main_api:asgi_app"]
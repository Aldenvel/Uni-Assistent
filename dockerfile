FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1

WORKDIR /app

# Systempakete minimal (nur wenn nötig). Hier keine Tools installieren, um die Angriffsfläche klein zu halten.
RUN apt-get update \
	&& apt-get install -y --no-install-recommends ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

# Abhängigkeiten installieren
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
	&& pip install -r /app/requirements.txt

# Code kopieren
COPY app.py /app/app.py
COPY warmup.py /app/warmup.py
COPY core /app/core
COPY templates /app/templates
COPY static /app/static

# Schreibverzeichnis vorbereiten (wird in Compose als Volume gemountet)
RUN mkdir -p /app/data \
	&& adduser --disabled-password --gecos "App User" --uid 1001 app \
	&& chown -R app:app /app

# Nicht als root ausführen
USER app

EXPOSE 5000

# Modelle vorab laden, dann Flask starten
CMD ["sh", "-c", "python /app/warmup.py && python /app/app.py"]
FROM python:3.12.12

# Update package lists and upgrade installed packages in one layer.
# Für Debian-/Ubuntu-basierte Python-Images (official images) verwenden wir apt-get.
RUN apt-get update \
	&& apt-get upgrade -y \
	&& rm -rf /var/lib/apt/lists/*

RUN mkdir /app

COPY requirements.txt /app/requirements.txt
COPY templates /app/templates
COPY app.py /app/app.py

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY Data /app/Data
COPY static /app/static
COPY core /app/core
CMD ["python", "/app/app.py"]
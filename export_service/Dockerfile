FROM python:3.11-slim

ENV PYTHONPATH=/app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    pkg-config \
    libpq-dev \
    postgresql-client \
    libmariadb-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared/
COPY export_service /app/

CMD ["python", "app.py"]
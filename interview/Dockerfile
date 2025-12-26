# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
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

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY interview /app/
COPY shared /app/shared/

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Make entrypoint script executable
COPY interview/scripts/entrypoint.sh /app/scripts/
RUN chmod +x /app/scripts/entrypoint.sh
# RUN dos2unix /app/scripts/entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
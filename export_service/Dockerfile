FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY shared /app/shared/
COPY export_service /app/

CMD ["python", "app.py"]
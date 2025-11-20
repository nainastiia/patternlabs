# Використовуємо офіційний образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо requirements.txt та .env
COPY requirements.txt .
COPY .env .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код програми
COPY app /app/app

# Запускаємо Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
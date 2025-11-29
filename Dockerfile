# Базовый образ Python
FROM python:3.10-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаём рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код проекта
COPY meetup_tg_bot/ /app/meetup_tg_bot/
WORKDIR /app/meetup_tg_bot

# Собираем статические файлы (будет выполнено при запуске)
# Создаём директории для статики и медиа
RUN mkdir -p /app/meetup_tg_bot/staticfiles /app/meetup_tg_bot/media

# Открываем порт
EXPOSE 8000

# Команда по умолчанию (можно переопределить в docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "meetuptg_bot.wsgi:application"]


# 🚀 Инструкция по деплою на сервер

## Требования

- Сервер с установленным Docker и Docker Compose
- Минимум 2GB RAM
- Открытые порты: 8000 (веб-сервер), 5432 (PostgreSQL, опционально)

## Шаг 1: Подготовка сервера

### Установка Docker и Docker Compose

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавляем пользователя в группу docker
sudo usermod -aG docker $USER

# Устанавливаем Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагружаемся или выходим/входим в систему
```

## Шаг 2: Клонирование репозитория

```bash
# Клонируем репозиторий
git clone https://github.com/Itsmyusername/dvmn_meetuptg_bot.git
cd dvmn_meetuptg_bot
```

## Шаг 3: Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
nano .env
```

Добавьте следующие переменные:

```env
# Django
SECRET_KEY=ваш-секретный-ключ-сгенерируйте-случайную-строку
DEBUG=False
ALLOWED_HOSTS=ваш-домен.ru,IP-адрес-сервера

# База данных PostgreSQL
POSTGRES_DB=meetup_bot_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=надежный-пароль-для-БД
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Telegram Bot
TELEGRAM_BOT_TOKEN=ваш-токен-бота-от-BotFather
```

**Важно:**
- `SECRET_KEY` - сгенерируйте случайную строку (можно использовать: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG=False` - обязательно для production!
- `ALLOWED_HOSTS` - укажите ваш домен и IP адрес сервера
- `POSTGRES_PASSWORD` - используйте надежный пароль

## Шаг 4: Сборка и запуск

```bash
# Собираем образы
docker-compose build

# Запускаем контейнеры
docker-compose up -d

# Проверяем статус
docker-compose ps

# Смотрим логи
docker-compose logs -f
```

## Шаг 5: Создание суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

## Шаг 6: Настройка Nginx (опционально, но рекомендуется)

Создайте конфигурацию Nginx:

```bash
sudo nano /etc/nginx/sites-available/meetup_bot
```

Добавьте:

```nginx
server {
    listen 80;
    server_name ваш-домен.ru;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /путь/к/проекту/meetup_tg_bot/staticfiles/;
    }

    location /media/ {
        alias /путь/к/проекту/meetup_tg_bot/media/;
    }
}
```

Активируйте конфигурацию:

```bash
sudo ln -s /etc/nginx/sites-available/meetup_bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Шаг 7: Настройка SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ваш-домен.ru
```

## Полезные команды

```bash
# Остановить контейнеры
docker-compose down

# Перезапустить контейнеры
docker-compose restart

# Обновить код и пересобрать
git pull
docker-compose build
docker-compose up -d

# Посмотреть логи
docker-compose logs -f web
docker-compose logs -f bot

# Выполнить миграции
docker-compose exec web python manage.py migrate

# Собрать статические файлы
docker-compose exec web python manage.py collectstatic --noinput

# Войти в контейнер
docker-compose exec web sh
```

## Мониторинг

Проверьте, что все сервисы работают:

```bash
# Статус контейнеров
docker-compose ps

# Использование ресурсов
docker stats

# Логи
docker-compose logs --tail=100
```

## Резервное копирование базы данных

```bash
# Создать бэкап
docker-compose exec db pg_dump -U postgres meetup_bot_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановить из бэкапа
docker-compose exec -T db psql -U postgres meetup_bot_db < backup_20240101_120000.sql
```

## Обновление проекта

```bash
# Получить последние изменения
git pull origin main

# Пересобрать и перезапустить
docker-compose build
docker-compose up -d

# Применить миграции (если есть новые)
docker-compose exec web python manage.py migrate
```


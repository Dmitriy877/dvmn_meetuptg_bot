# Meetup Telegram Bot

Django проект для Telegram бота Meetup.

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Itsmyusername/dvmn_meetuptg_bot.git
cd dvmn_meetuptg_bot
```

2. Создайте виртуальное окружение:
```bash
py -m venv venv
```

3. Активируйте виртуальное окружение:
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

4. Установите зависимости:
```bash
pip install -r requirements.txt
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Структура проекта

- `meetuptg_bot/` - основной пакет Django проекта
- `manage.py` - утилита для управления Django проектом
- `requirements.txt` - зависимости проекта

## Разработчики

- dzima_
- Dmitriy877
- Evst404


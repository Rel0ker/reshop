# 🚀 ReShop - Local Docker Deployment

Быстрое развертывание проекта ReShop локально через Docker.

## ⚡ Быстрый старт

### 1. Проверка готовности
```bash
python3 check_production_readiness.py
```

### 2. Развертывание
```bash
# Автоматическое развертывание
./deploy-local.sh

# Или через Makefile
make -f Makefile.local deploy
```

### 3. Проверка статуса
```bash
make -f Makefile.local status
```

## 🛠️ Основные команды

```bash
# Справка по командам
make -f Makefile.local help

# Запуск/остановка
make -f Makefile.local start
make -f Makefile.local stop
make -f Makefile.local restart

# Логи
make -f Makefile.local logs
make -f Makefile.local logs-backend
make -f Makefile.local logs-frontend
make -f Makefile.local logs-nginx

# Мониторинг
make -f Makefile.local status
make -f Makefile.local health-check
make -f Makefile.local monitor

# Управление базой данных
make -f Makefile.local migrate
make -f Makefile.local collectstatic
make -f Makefile.local createsuperuser
make -f Makefile.local shell

# Бэкап и восстановление
make -f Makefile.local backup
make -f Makefile.local restore FILE=backup_file.sql

# Обновление
make -f Makefile.local update

# Очистка
make -f Makefile.local clean
```

## 📁 Структура локального развертывания

```
reshop/
├── docker-compose.local.yml      # Локальный docker-compose
├── nginx.local.conf             # Локальная nginx конфигурация
├── Makefile.local               # Makefile для локального развертывания
├── deploy-local.sh              # Скрипт локального развертывания
├── env.production               # Переменные окружения
└── ssl/                         # SSL сертификаты (для HTTPS)
    ├── cert.pem
    └── key.pem
```

## 🌐 Доступные сервисы

После развертывания:

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Database**: localhost:5432
- **Redis**: localhost:6379

## 🔧 Настройка

### Переменные окружения

Файл `env.production` содержит все необходимые настройки:

```bash
# Database
POSTGRES_DB=reshop
POSTGRES_USER=reshop_user
POSTGRES_PASSWORD=reshop_password

# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Frontend
VITE_API_URL=http://localhost:8000/api
```

### SSL сертификаты

Для локального тестирования созданы самоподписанные сертификаты в папке `ssl/`.

## 🐳 Docker сервисы

### Backend (Django)
- **Порт**: 8000
- **Процессы**: 2 Gunicorn worker'а
- **База данных**: PostgreSQL
- **Кеш**: Redis

### Frontend (Vue.js)
- **Порт**: 3000
- **Сборка**: Production build
- **Сервер**: Nginx

### Database (PostgreSQL)
- **Порт**: 5432
- **Данные**: Docker volume
- **Пользователь**: reshop_user

### Redis
- **Порт**: 6379
- **Назначение**: Кеширование и сессии

### Nginx
- **Порт**: 80
- **Функции**: Reverse proxy, статические файлы

## 🔍 Мониторинг и логи

### Просмотр логов
```bash
# Все сервисы
make -f Makefile.local logs

# Конкретный сервис
make -f Makefile.local logs-backend
make -f Makefile.local logs-frontend
make -f Makefile.local logs-nginx
```

### Статус сервисов
```bash
make -f Makefile.local status
```

### Health check
```bash
make -f Makefile.local health-check
```

## 🆘 Устранение неполадок

### Частые проблемы

1. **Порт занят**
   ```bash
   # Проверить занятые порты
   lsof -i :80
   lsof -i :8000
   lsof -i :3000
   ```

2. **База данных не подключается**
   ```bash
   # Перезапустить только базу
   docker-compose -f docker-compose.local.yml restart db
   ```

3. **Frontend не собирается**
   ```bash
   # Очистить node_modules
   cd frontend-vue
   rm -rf node_modules package-lock.json
   npm ci
   cd ..
   ```

4. **Статические файлы не загружаются**
   ```bash
   make -f Makefile.local collectstatic
   ```

### Полезные команды

```bash
# Перезапуск конкретного сервиса
docker-compose -f docker-compose.local.yml restart backend

# Просмотр переменных окружения
docker-compose -f docker-compose.local.yml exec backend env

# Проверка подключения к базе
docker-compose -f docker-compose.local.yml exec backend python manage.py dbshell
```

## 🔄 Обновление

### Обновление кода
```bash
git pull origin main
make -f Makefile.local update
```

### Обновление зависимостей
```bash
# Backend
docker-compose -f docker-compose.local.yml exec backend pip install -r requirements.production.txt --upgrade

# Frontend
cd frontend-vue
npm update
npm run build:prod
cd ..
```

## 📊 Производительность

### Оптимизации включены:
- ✅ Gzip сжатие
- ✅ Кеширование статических файлов
- ✅ Оптимизация Docker образов
- ✅ Многопроцессный Gunicorn
- ✅ Redis кеширование

### Мониторинг ресурсов:
```bash
# Использование ресурсов
docker stats

# Мониторинг в реальном времени
make -f Makefile.local monitor
```

---

**Удачи с локальным развертыванием! 🎉**

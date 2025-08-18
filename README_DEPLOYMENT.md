# 🚀 ReShop - Deployment Guide

Полное руководство по развертыванию проекта ReShop.

## 🎯 Варианты развертывания

### 1. 🏠 Локальное развертывание (рекомендуется для начала)
- **Цель**: Тестирование и разработка
- **Сложность**: ⭐
- **Время**: 5-10 минут

### 2. 🌐 Продакшен развертывание
- **Цель**: Реальный сервер
- **Сложность**: ⭐⭐⭐
- **Время**: 15-30 минут

## 🏠 Локальное развертывание

### Быстрый старт
```bash
# 1. Проверка готовности
python3 check_production_readiness.py

# 2. Развертывание
./deploy-local.sh

# 3. Проверка статуса
make -f Makefile.local status
```

### Основные команды
```bash
# Справка
make -f Makefile.local help

# Управление
make -f Makefile.local start
make -f Makefile.local stop
make -f Makefile.local restart

# Логи и мониторинг
make -f Makefile.local logs
make -f Makefile.local status
make -f Makefile.local health-check
```

### Доступные сервисы
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

📖 [Подробная документация](README_LOCAL_DEPLOYMENT.md)

## 🌐 Продакшен развертывание

### Предварительные требования
- Домен и SSL сертификат
- VPS/сервер с Docker
- Минимум 2GB RAM, 20GB диска

### Быстрый старт
```bash
# 1. Проверка готовности
python3 check_production_readiness.py

# 2. Настройка переменных окружения
cp env.production .env.production
# Отредактируйте .env.production

# 3. Развертывание
make -f Makefile.production deploy
```

### Основные команды
```bash
# Справка
make -f Makefile.production help

# Управление
make -f Makefile.production start
make -f Makefile.production stop
make -f Makefile.production restart

# Мониторинг
make -f Makefile.production status
make -f Makefile.production health-check
```

📖 [Подробная документация](PRODUCTION_DEPLOYMENT.md)

## 🔧 Общие настройки

### Переменные окружения
```bash
# Обязательные
SECRET_KEY=your-secret-key
POSTGRES_PASSWORD=your-db-password
ALLOWED_HOSTS=yourdomain.com,localhost

# Опциональные
YOOKASSA_SHOP_ID=your-shop-id
YOOKASSA_SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
```

### Генерация секретного ключа
```bash
python3 generate_secret_key.py
```

## 🐳 Docker команды

### Локальное развертывание
```bash
# Запуск
docker-compose -f docker-compose.local.yml up -d

# Остановка
docker-compose -f docker-compose.local.yml down

# Логи
docker-compose -f docker-compose.local.yml logs -f
```

### Продакшен развертывание
```bash
# Запуск
docker-compose -f docker-compose.production.yml up -d

# Остановка
docker-compose -f docker-compose.production.yml down

# Логи
docker-compose -f docker-compose.production.yml logs -f
```

## 🔍 Мониторинг

### Health checks
```bash
# Локально
make -f Makefile.local health-check

# Продакшен
make -f Makefile.production health-check
```

### Логи
```bash
# Все сервисы
make -f Makefile.local logs

# Конкретный сервис
make -f Makefile.local logs-backend
make -f Makefile.local logs-frontend
make -f Makefile.local logs-nginx
```

### Статус
```bash
# Локально
make -f Makefile.local status

# Продакшен
make -f Makefile.production status
```

## 🆘 Устранение неполадок

### Частые проблемы

1. **Порты заняты**
   ```bash
   lsof -i :80
   lsof -i :8000
   lsof -i :3000
   ```

2. **База данных не подключается**
   ```bash
   # Проверить статус
   docker-compose -f docker-compose.local.yml ps db
   
   # Перезапустить
   docker-compose -f docker-compose.local.yml restart db
   ```

3. **Frontend не собирается**
   ```bash
   cd frontend-vue
   rm -rf node_modules package-lock.json
   npm ci
   npm run build:prod
   cd ..
   ```

4. **Статические файлы не загружаются**
   ```bash
   make -f Makefile.local collectstatic
   ```

### Полезные команды

```bash
# Очистка Docker
make -f Makefile.local clean

# Бэкап базы данных
make -f Makefile.local backup

# Восстановление
make -f Makefile.local restore FILE=backup_file.sql

# Django shell
make -f Makefile.local shell

# Создание суперпользователя
make -f Makefile.local createsuperuser
```

## 🔄 Обновление

### Обновление кода
```bash
git pull origin main

# Локально
make -f Makefile.local update

# Продакшен
make -f Makefile.production update
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

### Включенные оптимизации
- ✅ Gzip сжатие
- ✅ Кеширование Redis
- ✅ Оптимизация статических файлов
- ✅ Многопроцессный Gunicorn
- ✅ Nginx reverse proxy
- ✅ Docker оптимизации

### Мониторинг ресурсов
```bash
# Использование ресурсов
docker stats

# Мониторинг в реальном времени
make -f Makefile.local monitor
```

## 🛡️ Безопасность

### Настройки безопасности
- ✅ DEBUG отключен в продакшене
- ✅ HTTPS принудительно (в продакшене)
- ✅ HSTS заголовки
- ✅ Безопасные заголовки
- ✅ Rate limiting
- ✅ CORS настроен

### Рекомендации
1. Регулярно обновляйте зависимости
2. Используйте менеджер секретов
3. Настройте файрвол
4. Мониторьте логи
5. Делайте регулярные бэкапы

## 📚 Дополнительные ресурсы

- [Локальное развертывание](README_LOCAL_DEPLOYMENT.md)
- [Продакшен развертывание](PRODUCTION_DEPLOYMENT.md)
- [API документация](API.md)
- [Тестирование](TESTING.md)

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи: `make -f Makefile.local logs`
2. Убедитесь в корректности настроек
3. Проверьте документацию
4. Создайте issue в репозитории

---

**Удачи с развертыванием! 🎉**

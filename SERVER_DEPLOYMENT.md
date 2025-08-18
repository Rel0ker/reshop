# 🚀 Развертывание на сервере 89.185.85.178

## ⚡ Быстрый старт

### 1. Подключение к серверу
```bash
ssh root@89.185.85.178
# Пароль: goWd5arjkjtU
```

### 2. Автоматическое развертывание
```bash
# Скачать скрипт развертывания
wget https://raw.githubusercontent.com/your-username/reshop/main/deploy-server.sh

# Сделать исполняемым
chmod +x deploy-server.sh

# Запустить развертывание
./deploy-server.sh
```

## 🔧 Ручное развертывание

### 1. Установка Docker
```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl start docker
systemctl enable docker

# Установка Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 2. Клонирование проекта
```bash
git clone https://github.com/your-username/reshop.git
cd reshop
```

### 3. Сборка и запуск
```bash
# Сборка frontend
cd frontend-vue
npm ci
npm run build:prod
cd ..

# Запуск сервисов
docker-compose -f docker-compose.server.yml up -d

# Миграции
docker-compose -f docker-compose.server.yml exec -T backend python manage.py migrate

# Статические файлы
docker-compose -f docker-compose.server.yml exec -T backend python manage.py collectstatic --noinput
```

## 🌐 Доступные сервисы

- **Frontend**: http://89.185.85.178
- **Backend API**: http://89.185.85.178:8000/api/
- **Admin Panel**: http://89.185.85.178:8000/admin/

## 🛠️ Управление сервисами

```bash
# Статус
docker-compose -f docker-compose.server.yml ps

# Логи
docker-compose -f docker-compose.server.yml logs -f

# Перезапуск
docker-compose -f docker-compose.server.yml restart

# Остановка
docker-compose -f docker-compose.server.yml down
```

## 🔍 Устранение неполадок

### Проверка логов
```bash
# Все сервисы
docker-compose -f docker-compose.server.yml logs

# Конкретный сервис
docker-compose -f docker-compose.server.yml logs backend
docker-compose -f docker-compose.server.yml logs frontend
```

### Проверка статуса
```bash
docker-compose -f docker-compose.server.yml ps
```

### Проверка портов
```bash
netstat -tlnp | grep :80
netstat -tlnp | grep :8000
netstat -tlnp | grep :3000
```

## 🆘 Частые проблемы

1. **Сервисы не запускаются**
   - Проверьте логи: `docker-compose -f docker-compose.server.yml logs`
   - Убедитесь, что Docker запущен: `systemctl status docker`

2. **Порты недоступны**
   - Проверьте файрвол: `ufw status`
   - Откройте порты: `ufw allow 80`, `ufw allow 8000`

3. **База данных не подключается**
   - Проверьте статус PostgreSQL: `docker-compose -f docker-compose.server.yml ps db`
   - Перезапустите: `docker-compose -f docker-compose.server.yml restart db`

## 📋 Полезные команды

```bash
# Мониторинг ресурсов
docker stats

# Очистка Docker
docker system prune -a

# Бэкап базы данных
docker-compose -f docker-compose.server.yml exec -T db pg_dump -U reshop_user reshop > backup.sql

# Django shell
docker-compose -f docker-compose.server.yml exec backend python manage.py shell
```

---

**Удачи с развертыванием! 🎉**

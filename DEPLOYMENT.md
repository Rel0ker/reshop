# Deployment Guide

Руководство по развертыванию Reshop - Digital Marketplace.

## 🚀 Обзор

Этот документ описывает процесс развертывания Reshop в production среде с использованием:
- PostgreSQL для базы данных
- Redis для кэширования
- Gunicorn для WSGI сервера
- Nginx для проксирования и статических файлов
- Supervisor для управления процессами
- Let's Encrypt для SSL сертификатов

## 🏗️ Архитектура

```
Internet → Nginx → Gunicorn → Django → PostgreSQL
                ↓
            Static Files
                ↓
            Redis Cache
```

## 📋 Требования

### Система
- Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- 2GB RAM минимум
- 20GB свободного места
- Root доступ или sudo права

### Программное обеспечение
- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Nginx 1.18+
- Supervisor 4.0+

## 🔧 Подготовка сервера

### 1. Обновление системы

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
# или
sudo dnf update -y
```

### 2. Установка базовых пакетов

```bash
# Ubuntu/Debian
sudo apt install -y curl wget git build-essential python3.11 python3.11-venv python3.11-dev

# CentOS/RHEL
sudo yum install -y curl wget git gcc python3.11 python3.11-devel
```

### 3. Создание пользователя

```bash
# Создание пользователя для приложения
sudo useradd -r -s /bin/false reshop
sudo mkdir -p /opt/reshop
sudo chown reshop:reshop /opt/reshop
```

## 🗄️ База данных

### PostgreSQL

```bash
# Ubuntu/Debian
sudo apt install -y postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install -y postgresql postgresql-server postgresql-contrib
sudo postgresql-setup initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### Настройка PostgreSQL

```bash
# Переключение на пользователя postgres
sudo -u postgres psql

# Создание пользователя и базы данных
CREATE USER reshop_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE reshop OWNER reshop_user;
GRANT ALL PRIVILEGES ON DATABASE reshop TO reshop_user;
\q

# Настройка аутентификации
sudo nano /etc/postgresql/*/main/pg_hba.conf
# Добавьте: local reshop reshop_user md5

# Перезапуск PostgreSQL
sudo systemctl restart postgresql
```

## 🔴 Redis

```bash
# Ubuntu/Debian
sudo apt install -y redis-server

# CentOS/RHEL
sudo yum install -y redis
sudo systemctl enable redis
sudo systemctl start redis

# Настройка Redis
sudo nano /etc/redis/redis.conf
# Измените: bind 127.0.0.1
sudo systemctl restart redis
```

## 🌐 Nginx

```bash
# Ubuntu/Debian
sudo apt install -y nginx

# CentOS/RHEL
sudo yum install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Конфигурация Nginx

```bash
# Копирование конфигурации
sudo cp nginx.conf /etc/nginx/sites-available/reshop
sudo ln -s /etc/nginx/sites-available/reshop /etc/nginx/sites-enabled/

# Удаление default сайта
sudo rm /etc/nginx/sites-enabled/default

# Тестирование конфигурации
sudo nginx -t

# Перезапуск Nginx
sudo systemctl restart nginx
```

## 🐍 Python и Django

### 1. Клонирование приложения

```bash
# Переключение на пользователя reshop
sudo -u reshop bash

# Клонирование репозитория
cd /opt
git clone https://github.com/rel0ker/reshop.git
cd reshop

# Создание виртуального окружения
python3.11 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 2. Настройка переменных окружения

```bash
# Копирование примера
cp env.example .env

# Редактирование .env
nano .env
```

```bash
# .env
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://reshop_user:your_secure_password@localhost:5432/reshop
REDIS_URL=redis://localhost:6379/0
YOOKASSA_SHOP_ID=your_shop_id
YOOKASSA_SECRET_KEY=your_secret_key
```

### 3. Миграции и статические файлы

```bash
# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Сборка статических файлов
python manage.py collectstatic --noinput

# Создание директории для медиа
mkdir -p media
chmod 755 media
```

## 🚀 Gunicorn

### Установка и настройка

```bash
# Установка Gunicorn
pip install gunicorn

# Создание конфигурации
nano gunicorn.conf.py
```

```python
# gunicorn.conf.py
bind = "unix:/opt/reshop/reshop.sock"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
preload_app = True
```

### Supervisor

```bash
# Установка Supervisor
sudo apt install -y supervisor

# Создание конфигурации
sudo nano /etc/supervisor/conf.d/reshop.conf
```

```ini
[program:reshop]
command=/opt/reshop/venv/bin/gunicorn -c /opt/reshop/gunicorn.conf.py digital_marketplace.wsgi:application
directory=/opt/reshop
user=reshop
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/reshop/gunicorn.log
stderr_logfile=/var/log/reshop/gunicorn_error.log
environment=HOME="/opt/reshop",USER="reshop"
```

```bash
# Создание директории для логов
sudo mkdir -p /var/log/reshop
sudo chown reshop:reshop /var/log/reshop

# Перезапуск Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start reshop
```

## 🔒 SSL сертификаты

### Let's Encrypt

```bash
# Установка Certbot
sudo apt install -y certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Автоматическое обновление
sudo crontab -e
# Добавьте: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔧 Мониторинг и логирование

### Логи

```bash
# Django логи
tail -f /var/log/reshop/django.log

# Gunicorn логи
tail -f /var/log/reshop/gunicorn.log

# Nginx логи
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Supervisor логи
tail -f /var/log/supervisor/supervisord.log
```

### Мониторинг

```bash
# Статус сервисов
sudo systemctl status nginx postgresql redis
sudo supervisorctl status

# Использование ресурсов
htop
df -h
free -h

# Проверка портов
sudo netstat -tlnp
```

## 🛡️ Безопасность

### Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# iptables (CentOS)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo service iptables save
```

### Обновления

```bash
# Автоматические обновления
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# Обновление зависимостей
cd /opt/reshop
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 📊 Резервное копирование

### База данных

```bash
#!/bin/bash
# backup_db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/reshop/backups"
DB_NAME="reshop"
DB_USER="reshop_user"

mkdir -p $BACKUP_DIR
pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/reshop_$DATE.sql

# Сжатие
gzip $BACKUP_DIR/reshop_$DATE.sql

# Удаление старых резервных копий (старше 30 дней)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

### Медиа файлы

```bash
#!/bin/bash
# backup_media.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/reshop/backups"
MEDIA_DIR="/opt/reshop/media"

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $MEDIA_DIR .

# Удаление старых резервных копий (старше 30 дней)
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +30 -delete
```

### Автоматизация

```bash
# Добавление в crontab
sudo crontab -e

# Ежедневное резервное копирование в 2:00
0 2 * * * /opt/reshop/backup_db.sh
30 2 * * * /opt/reshop/backup_media.sh
```

## 🚨 Troubleshooting

### Частые проблемы

#### 1. 500 ошибка
```bash
# Проверьте логи
tail -f /var/log/reshop/gunicorn.log

# Проверьте права доступа
ls -la /opt/reshop/
sudo chown -R reshop:reshop /opt/reshop
```

#### 2. Статические файлы не загружаются
```bash
# Пересоберите статические файлы
cd /opt/reshop
source venv/bin/activate
python manage.py collectstatic --noinput

# Проверьте права
sudo chmod -R 755 /opt/reshop/static/
```

#### 3. База данных недоступна
```bash
# Проверьте статус PostgreSQL
sudo systemctl status postgresql

# Проверьте подключение
sudo -u postgres psql -c "\l"
```

### Полезные команды

```bash
# Перезапуск всех сервисов
sudo systemctl restart nginx postgresql redis
sudo supervisorctl restart reshop

# Проверка конфигурации
sudo nginx -t
sudo supervisorctl reread

# Очистка кэша
redis-cli FLUSHALL
```

## 📈 Оптимизация

### База данных

```sql
-- Создание индексов
CREATE INDEX idx_product_title ON core_product(title);
CREATE INDEX idx_product_description ON core_product(description);
CREATE INDEX idx_order_created ON core_order(created_at);
CREATE INDEX idx_user_email ON core_user(email);

-- Анализ производительности
ANALYZE core_product;
ANALYZE core_order;
ANALYZE core_user;
```

### Кэширование

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Использование кэша в views
from django.core.cache import cache

def get_products():
    products = cache.get('products')
    if products is None:
        products = Product.objects.all()
        cache.set('products', products, 300)  # 5 минут
    return products
```

### Gunicorn оптимизация

```python
# gunicorn.conf.py
bind = "unix:/opt/reshop/reshop.sock"
workers = (2 * multiprocessing.cpu_count()) + 1
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
preload_app = True
```

## 🔄 Обновления

### Автоматическое обновление

```bash
#!/bin/bash
# update.sh

cd /opt/reshop

# Создание резервной копии
./backup_db.sh
./backup_media.sh

# Обновление кода
git pull origin main

# Обновление зависимостей
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Миграции
python manage.py migrate

# Статические файлы
python manage.py collectstatic --noinput

# Перезапуск
sudo supervisorctl restart reshop

echo "Update completed!"
```

### Ручное обновление

```bash
# Остановка сервисов
sudo supervisorctl stop reshop

# Обновление
cd /opt/reshop
git pull origin main
source venv/bin/activate
pip install --upgrade -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Запуск
sudo supervisorctl start reshop
```

## 📚 Дополнительные ресурсы

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [Nginx Configuration](https://nginx.org/en/docs/)
- [PostgreSQL Administration](https://www.postgresql.org/docs/current/admin.html)
- [Redis Documentation](https://redis.io/documentation)
- [Supervisor Documentation](http://supervisord.org/)

## 🆘 Поддержка

Если у вас возникли проблемы:

1. Проверьте логи сервисов
2. Убедитесь, что все сервисы запущены
3. Проверьте права доступа к файлам
4. Создайте Issue в репозитории

---

Удачи с production развертыванием! 🚀

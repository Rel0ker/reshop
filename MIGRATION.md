# Migration Guide

Руководство по миграции между версиями Reshop.

## 🔄 Миграция с версии 0.1.x на 1.0.0

### Breaking Changes

#### 1. Структура базы данных

- Добавлены новые поля в модель `Order`
- Изменена структура `ProductImage`
- Добавлены новые модели для комментариев

#### 2. API изменения

- Изменены URL endpoints для платежей
- Добавлены новые поля в ответы API
- Изменена структура аутентификации

#### 3. Frontend изменения

- Обновлены компоненты для работы с новым API
- Изменена структура состояния приложения
- Добавлены новые страницы и функции

### Пошаговая миграция

#### Backend

1. **Создайте резервную копию:**
   ```bash
   # База данных
   python manage.py dumpdata > backup_old.json
   
   # Медиа файлы
   tar -czf media_backup.tar.gz media/
   ```

2. **Обновите код:**
   ```bash
   git pull origin main
   pip install -r requirements.txt
   ```

3. **Примените миграции:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Проверьте целостность:**
   ```bash
   python manage.py check
   python manage.py test
   ```

#### Frontend

1. **Обновите зависимости:**
   ```bash
   cd frontend-vue
   npm install
   ```

2. **Проверьте совместимость:**
   ```bash
   npm run build
   npm test
   ```

3. **Обновите конфигурацию:**
   - Проверьте API endpoints
   - Обновите переменные окружения
   - Проверьте настройки сборки

### Откат изменений

Если что-то пошло не так:

```bash
# Восстановление базы данных
python manage.py loaddata backup_old.json

# Восстановление медиа файлов
tar -xzf media_backup.tar.gz

# Откат к предыдущей версии
git checkout v0.1.0
```

## 📊 Миграция данных

### Преобразование существующих данных

#### 1. Продукты

```python
# Скрипт миграции продуктов
from core.models import Product, ProductImage

def migrate_products():
    products = Product.objects.all()
    
    for product in products:
        # Создание ProductImage для существующих изображений
        if product.image_url:
            ProductImage.objects.create(
                product=product,
                image=product.image_url,
                is_main=True
            )
        
        # Обновление полей
        if not hasattr(product, 'seller_info'):
            product.seller_info = "Информация о продавце"
            product.save()
        
        if not hasattr(product, 'usage_instructions'):
            product.usage_instructions = "Инструкция по использованию"
            product.save()
```

#### 2. Заказы

```python
# Скрипт миграции заказов
from core.models import Order

def migrate_orders():
    orders = Order.objects.all()
    
    for order in orders:
        # Добавление недостающих полей
        if not hasattr(order, 'comment'):
            order.comment = ""
            order.save()
        
        if not hasattr(order, 'receipt_email'):
            order.receipt_email = order.buyer.email
            order.save()
```

#### 3. Пользователи

```python
# Скрипт миграции пользователей
from core.models import User

def migrate_users():
    users = User.objects.all()
    
    for user in users:
        # Установка роли по умолчанию
        if not hasattr(user, 'role'):
            user.role = User.Role.BUYER
            user.save()
```

### Запуск миграции

```bash
# Создайте файл migrate_data.py
python manage.py shell < migrate_data.py

# Или запустите через Django команду
python manage.py migrate_data
```

## 🔧 Настройка после миграции

### 1. Проверка функциональности

- [ ] Аутентификация работает
- [ ] Продукты отображаются
- [ ] Заказы создаются
- [ ] Платежи обрабатываются
- [ ] Поиск функционирует
- [ ] Комментарии работают

### 2. Настройка новых функций

#### Yookassa

```bash
# Добавьте в .env
YOOKASSA_SHOP_ID=your_shop_id
YOOKASSA_SECRET_KEY=your_secret_key
```

#### Поиск

```bash
# Проверьте настройки поиска
python manage.py shell
>>> from core.models import Product
>>> Product.objects.filter(title__icontains='test').count()
```

#### Изображения

```bash
# Настройте медиа файлы
python manage.py collectstatic
chmod -R 755 media/
```

### 3. Мониторинг

```bash
# Проверьте логи
tail -f debug.log

# Проверьте статус сервисов
python manage.py check
```

## 🚨 Проблемы и решения

### Частые проблемы

#### 1. Ошибки миграции

```bash
# Ошибка: "no such column"
python manage.py migrate --fake-initial

# Ошибка: "table already exists"
python manage.py migrate --fake
```

#### 2. Проблемы с изображениями

```bash
# Пересоздание ProductImage
python manage.py shell
>>> from core.models import Product, ProductImage
>>> ProductImage.objects.all().delete()
>>> # Запустите скрипт миграции изображений
```

#### 3. Проблемы с API

```bash
# Проверьте URL конфигурацию
python manage.py show_urls

# Проверьте права доступа
python manage.py check --deploy
```

### Отладка

```bash
# Включите отладку
DEBUG = True

# Проверьте логи
python manage.py shell
>>> import logging
>>> logging.getLogger('django').setLevel(logging.DEBUG)
```

## 📈 Производительность

### После миграции

1. **Индексы базы данных:**
   ```sql
   -- Создание индексов для поиска
   CREATE INDEX idx_product_title ON core_product(title);
   CREATE INDEX idx_product_description ON core_product(description);
   ```

2. **Кэширование:**
   ```python
   # settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
       }
   }
   ```

3. **Оптимизация запросов:**
   ```python
   # Используйте select_related и prefetch_related
   products = Product.objects.select_related('seller').prefetch_related('images')
   ```

## 🔄 Автоматизация миграции

### Скрипт миграции

```bash
#!/bin/bash
# migrate.sh

echo "Starting migration..."

# Создание резервной копии
echo "Creating backup..."
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# Обновление кода
echo "Updating code..."
git pull origin main

# Обновление зависимостей
echo "Updating dependencies..."
pip install -r requirements.txt

# Применение миграций
echo "Applying migrations..."
python manage.py migrate

# Сборка статических файлов
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Проверка
echo "Running checks..."
python manage.py check

echo "Migration completed!"
```

### Запуск

```bash
chmod +x migrate.sh
./migrate.sh
```

## 📚 Дополнительные ресурсы

- [Django Migrations](https://docs.djangoproject.com/en/stable/topics/migrations/)
- [Database Operations](https://docs.djangoproject.com/en/stable/ref/django-admin/#dbshell)
- [Data Migration](https://docs.djangoproject.com/en/stable/howto/writing-migrations/#data-migrations)

---

Удачи с миграцией! 🚀


# Reshop - Digital Marketplace

[![Version](https://img.shields.io/badge/version-3.3.1-blue.svg)](https://github.com/rel0ker/reshop)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Vue.js](https://img.shields.io/badge/vue.js-3+-green.svg)](https://vuejs.org)
[![Django](https://img.shields.io/badge/django-5+-green.svg)](https://djangoproject.com)

Современная платформа для цифрового маркетплейса с поддержкой Vue.js фронтенда и Django бэкенда.

## 🚀 Быстрый старт

```bash
# Клонирование
git clone github.com/rel0ker/reshop
cd reshop

# Backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
cp env.example .env
python manage.py migrate
python manage.py runserver

# Frontend (в новом терминале)
cd frontend-vue
npm install
npm run dev
```

**Готово!** Откройте http://localhost:5173 в браузере.

## 🌟 Особенности

- **Frontend**: Vue.js 3 + TypeScript + Tailwind CSS
- **Backend**: Django 5 + Django REST Framework
- **Аутентификация**: JWT токены
- **Платежи**: Интеграция с Yookassa
- **Поиск**: Полнотекстовый поиск по товарам
- **Изображения**: Загрузка и управление изображениями товаров
- **Комментарии**: Система отзывов и рейтингов

## 📋 Требования

- Python 3.11+
- Node.js 18+
- npm или yarn

## 🛠️ Установка

### 1. Клонирование репозитория

```bash
git clone github.com/rel0ker/reshop
cd reshop
```

### 2. Backend (Django)

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Копирование примера переменных окружения
cp env.example .env

# Редактирование .env файла с вашими настройками
# Особенно важно настроить SECRET_KEY и YOOKASSA_* ключи

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера разработки
python manage.py runserver
```

### 3. Frontend (Vue.js)

```bash
cd frontend-vue

# Установка зависимостей
npm install

# Запуск сервера разработки
npm run dev
```

## ⚙️ Настройка

### Переменные окружения

Создайте файл `.env` на основе `env.example`:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Yookassa Settings
YOOKASSA_SHOP_ID=your_shop_id_here
YOOKASSA_SECRET_KEY=your_secret_key_here
```

### Yookassa

Для работы с платежами необходимо:

1. Зарегистрироваться в [Yookassa](https://yookassa.ru/)
2. Получить Shop ID и Secret Key
3. Добавить их в `.env` файл

## 🗄️ Структура проекта

```
reshop/
├── core/                    # Django приложение
│   ├── models.py           # Модели данных
│   ├── views.py            # API представления
│   ├── serializers.py      # Сериализаторы
│   └── urls.py             # URL маршруты
├── digital_marketplace/     # Django проект
│   ├── settings.py         # Настройки
│   └── urls.py             # Основные URL
├── frontend-vue/           # Vue.js приложение
│   ├── src/
│   │   ├── components/     # Vue компоненты
│   │   ├── pages/          # Страницы
│   │   ├── composables/    # Composables
│   │   └── router/         # Маршрутизация
│   └── package.json
├── requirements.txt         # Python зависимости
└── README.md
```

## 🔧 API Endpoints

### Аутентификация
- `POST /auth/login/` - Вход в систему
- `POST /auth/register/` - Регистрация
- `POST /auth/refresh/` - Обновление токена

### Товары
- `GET /products/` - Список товаров
- `GET /products/{id}/` - Детали товара
- `POST /products/` - Создание товара (только продавцы)
- `PUT /products/{id}/` - Обновление товара (только владелец)

### Заказы
- `POST /payments/` - Создание заказа и платежа
- `GET /orders/` - Список заказов пользователя

### Комментарии
- `GET /comments/?product_id={id}` - Комментарии к товару
- `POST /comments/` - Добавление комментария

## 🚀 Развертывание

### Production

1. Установите `DEBUG=False` в `.env`
2. Настройте `ALLOWED_HOSTS` для вашего домена
3. Используйте PostgreSQL вместо SQLite
4. Настройте статические файлы: `python manage.py collectstatic`
5. Используйте Gunicorn или uWSGI для WSGI сервера
6. Настройте Nginx для проксирования

### Docker

```bash
# Сборка образов
docker-compose build

# Запуск
docker-compose up -d
```

## 📚 Документация

Проект включает подробную документацию:

- **[QUICKSTART.md](QUICKSTART.md)** - Быстрый старт за 5 минут
- **[API.md](API.md)** - Полная документация по API
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Руководство по развертыванию
- **[PRODUCTION.md](PRODUCTION.md)** - Production развертывание
- **[TESTING.md](TESTING.md)** - Руководство по тестированию
- **[MIGRATION.md](MIGRATION.md)** - Миграция между версиями
- **[SECURITY.md](SECURITY.md)** - Политика безопасности
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Как внести вклад в проект

## 🛠️ Утилиты разработки

### Make команды

```bash
# Полная настройка
make setup

# Запуск обоих серверов
make dev

# Остановка
make stop-dev

# Справка
make help
```

### Docker команды

```bash
# Сборка
make docker-build

# Запуск
make docker-up

# Остановка
make docker-down
```

## 💡 Примеры использования

### Создание продукта

```python
import requests

# Аутентификация
response = requests.post('http://localhost:8000/api/auth/login/', {
    'username': 'seller',
    'password': 'password'
})
token = response.json()['access']

# Создание продукта
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:8000/api/products/', {
    'title': 'Новый продукт',
    'description': 'Описание продукта',
    'price': '99.99'
}, headers=headers)
```

### Поиск продуктов

```javascript
// Поиск по названию
const response = await fetch('/api/products/?search=laptop&min_price=100');
const { results: products } = await response.json();

// Фильтрация по категории
const response = await fetch('/api/products/?category=electronics&ordering=price');
const { results: products } = await response.json();
```

## 🎯 Основные функции

### Для покупателей
- 📱 Просмотр каталога товаров
- 🔍 Поиск и фильтрация
- 🛒 Создание заказов
- 💳 Оплата через Yookassa
- 📝 Оставление отзывов
- ❤️ Добавление в избранное

### Для продавцов
- 🏪 Создание магазина
- 📦 Управление товарами
- 🖼️ Загрузка изображений
- 📊 Просмотр заказов
- 💰 Управление продажами

### Для администраторов
- 👥 Управление пользователями
- 🛡️ Модерация контента
- 📈 Аналитика и отчеты
- ⚙️ Настройка системы

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 🆘 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте [Issues](https://github.com/rel0ker/reshop/issues)
2. Создайте новый Issue с описанием проблемы
3. Укажите версии Python, Django и Vue.js

## 🔒 Безопасность

- Никогда не коммитьте `.env` файлы
- Регулярно обновляйте зависимости
- Используйте HTTPS в production
- Настройте CORS правильно для вашего домена

## 📊 Статус проекта

- **Версия**: 3.3.1
- **Статус**: Beta
- **Последнее обновление**: Август 2024
- **Поддерживаемые версии**: Python 3.11+, Django 5+, Vue.js 3+

## 🎯 Roadmap

- [ ] Мобильное приложение
- [ ] Аналитика и отчеты
- [ ] Мультиязычность
- [ ] Расширенная система уведомлений
- [ ] Интеграция с другими платежными системами

## 🌟 Звезды и форки

Если проект вам понравился, поставьте звезду ⭐ и сделайте форк! Это поможет проекту развиваться.

## 📞 Контакты

- **Автор**: [rel0ker](https://github.com/rel0ker)
- **Email**: rel0ker@ya.ru
- **GitHub**: [github.com/rel0ker/reshop](https://github.com/rel0ker/reshop)

---

Добро пожаловать в Reshop! 🎉
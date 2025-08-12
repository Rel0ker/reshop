# API Documentation

Полная документация по API Reshop - Digital Marketplace.

## 🚀 Обзор

Reshop API предоставляет RESTful интерфейс для:
- Управления пользователями и аутентификации
- Создания и управления продуктами
- Обработки заказов и платежей
- Управления комментариями и отзывами
- Поиска и фильтрации продуктов

## 🔐 Аутентификация

### JWT токены

API использует JWT (JSON Web Tokens) для аутентификации.

#### Получение токена

```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Ответ:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": "user_id",
        "username": "username",
        "email": "user@example.com",
        "role": "buyer"
    }
}
```

#### Обновление токена

```http
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

#### Использование токена

```http
GET /api/products/
Authorization: Bearer your_access_token
```

### Роли пользователей

- **buyer** - покупатель, может просматривать продукты и создавать заказы
- **seller** - продавец, может создавать и управлять продуктами
- **admin** - администратор, полный доступ

## 👥 Пользователи

### Регистрация

```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "newuser",
    "email": "user@example.com",
    "password": "secure_password",
    "role": "buyer"
}
```

### Профиль пользователя

```http
GET /api/auth/me/
Authorization: Bearer your_access_token
```

**Ответ:**
```json
{
    "id": "user_id",
    "username": "username",
    "email": "user@example.com",
    "role": "buyer",
    "date_joined": "2024-01-01T00:00:00Z"
}
```

### Обновление профиля

```http
PUT /api/auth/me/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "email": "newemail@example.com"
}
```

## 🛍️ Продукты

### Список продуктов

```http
GET /api/products/
```

**Параметры запроса:**
- `search` - поиск по названию и описанию
- `category` - фильтр по категории
- `min_price` - минимальная цена
- `max_price` - максимальная цена
- `ordering` - сортировка (price, -price, created_at, -created_at)
- `page` - номер страницы
- `page_size` - размер страницы

**Пример:**
```http
GET /api/products/?search=laptop&min_price=100&ordering=price&page=1&page_size=20
```

**Ответ:**
```json
{
    "count": 100,
    "next": "http://api.example.com/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": "product_id",
            "title": "Laptop",
            "description": "Powerful laptop",
            "price": "999.99",
            "category": "electronics",
            "seller": {
                "id": "seller_id",
                "username": "seller_name"
            },
            "images": [
                {
                    "id": "image_id",
                    "image": "http://api.example.com/media/products/laptop.jpg",
                    "is_main": true
                }
            ],
            "rating": 4.5,
            "reviews_count": 25,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### Детали продукта

```http
GET /api/products/{id}/
```

**Ответ:**
```json
{
    "id": "product_id",
    "title": "Laptop",
    "description": "Powerful laptop with high performance",
    "price": "999.99",
    "category": "electronics",
    "seller": {
        "id": "seller_id",
        "username": "seller_name",
        "email": "seller@example.com"
    },
    "images": [
        {
            "id": "image_id",
            "image": "http://api.example.com/media/products/laptop.jpg",
            "is_main": true
        }
    ],
    "rating": 4.5,
    "reviews_count": 25,
    "seller_info": "Professional electronics seller",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### Создание продукта (только продавцы)

```http
POST /api/products/
Authorization: Bearer your_access_token
Content-Type: multipart/form-data

{
    "title": "New Product",
    "description": "Product description",
    "price": "99.99",
    "category": "electronics",
    "seller_info": "Seller information",
    "images": [image_file1, image_file2]
}
```

### Обновление продукта (только владелец)

```http
PUT /api/products/{id}/
Authorization: Bearer your_access_token
Content-Type: multipart/form-data

{
    "title": "Updated Product",
    "description": "Updated description",
    "price": "89.99"
}
```

### Удаление продукта (только владелец)

```http
DELETE /api/products/{id}/
Authorization: Bearer your_access_token
```

## 🛒 Заказы

### Создание заказа

```http
POST /api/payments/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "product": "product_id",
    "quantity": 2,
    "comment": "Please deliver quickly",
    "receipt_email": "buyer@example.com"
}
```

**Ответ:**
```json
{
    "id": "order_id",
    "product": {
        "id": "product_id",
        "title": "Product Title",
        "price": "99.99"
    },
    "quantity": 2,
    "comment": "Please deliver quickly",
    "receipt_email": "buyer@example.com",
    "buyer": {
        "id": "buyer_id",
        "username": "buyer_name"
    },
    "status": "pending",
    "created_at": "2024-01-01T00:00:00Z",
    "total_amount": "199.98",
    "payment_id": "payment_id",
    "payment_url": "https://yoomoney.ru/checkout/payments/v2/contract",
    "amount": "199.98",
    "currency": "RUB",
    "payment_status": "pending"
}
```

### Список заказов пользователя

```http
GET /api/orders/
Authorization: Bearer your_access_token
```

**Параметры запроса:**
- `status` - фильтр по статусу (pending, paid, completed, canceled)
- `ordering` - сортировка (created_at, -created_at)

### Детали заказа

```http
GET /api/orders/{id}/
Authorization: Bearer your_access_token
```

## 💬 Комментарии

### Список комментариев к продукту

```http
GET /api/comments/?product_id={product_id}
```

**Ответ:**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "comment_id",
            "product": "product_id",
            "user": {
                "id": "user_id",
                "username": "username"
            },
            "text": "Great product!",
            "rating": 5,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### Создание комментария

```http
POST /api/comments/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "product": "product_id",
    "text": "Excellent product, highly recommend!",
    "rating": 5
}
```

### Обновление комментария (только автор)

```http
PUT /api/comments/{id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "text": "Updated comment text",
    "rating": 4
}
```

### Удаление комментария (только автор)

```http
DELETE /api/comments/{id}/
Authorization: Bearer your_access_token
```

## 🔍 Поиск и фильтрация

### Поиск продуктов

```http
GET /api/products/?search=query
```

**Особенности поиска:**
- Поиск по названию и описанию
- Регистронезависимый
- Поддержка специальных символов
- Автоматическое экранирование

### Фильтрация по цене

```http
GET /api/products/?min_price=100&max_price=1000
```

### Фильтрация по категории

```http
GET /api/products/?category=electronics
```

### Сортировка

```http
GET /api/products/?ordering=price          # По возрастанию цены
GET /api/products/?ordering=-price         # По убыванию цены
GET /api/products/?ordering=created_at     # По дате создания (новые)
GET /api/products/?ordering=-created_at    # По дате создания (старые)
```

## 📱 Пагинация

API использует пагинацию по страницам.

**Параметры:**
- `page` - номер страницы (начиная с 1)
- `page_size` - количество элементов на странице (по умолчанию 20)

**Пример:**
```http
GET /api/products/?page=2&page_size=10
```

**Ответ:**
```json
{
    "count": 100,
    "next": "http://api.example.com/products/?page=3&page_size=10",
    "previous": "http://api.example.com/products/?page=1&page_size=10",
    "results": [...]
}
```

## 🚨 Обработка ошибок

### Стандартные HTTP коды

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

### Формат ошибок

```json
{
    "error": "Error message",
    "detail": "Detailed error description",
    "code": "ERROR_CODE"
}
```

### Примеры ошибок

#### Валидация данных

```json
{
    "title": ["This field is required."],
    "price": ["Enter a valid price."]
}
```

#### Аутентификация

```json
{
    "detail": "Authentication credentials were not provided."
}
```

#### Права доступа

```json
{
    "detail": "You do not have permission to perform this action."
}
```

## 🔒 Права доступа

### Продукты

| Действие | Покупатель | Продавец | Админ |
|----------|------------|----------|-------|
| Просмотр | ✅ | ✅ | ✅ |
| Создание | ❌ | ✅ | ✅ |
| Редактирование | ❌ | Свои | ✅ |
| Удаление | ❌ | Свои | ✅ |

### Заказы

| Действие | Покупатель | Продавец | Админ |
|----------|------------|----------|-------|
| Создание | ✅ | ❌ | ✅ |
| Просмотр | Свои | Связанные | ✅ |
| Обновление | ❌ | Статус | ✅ |

### Комментарии

| Действие | Покупатель | Продавец | Админ |
|----------|------------|----------|-------|
| Создание | ✅ | ✅ | ✅ |
| Редактирование | Свои | Свои | ✅ |
| Удаление | Свои | Свои | ✅ |

## 📊 Rate Limiting

API использует ограничение скорости запросов:

- **Аутентификация**: 5 запросов в минуту
- **API endpoints**: 10 запросов в секунду
- **Загрузка файлов**: 2 запроса в минуту

## 🔄 Webhooks

### Yookassa webhook

```http
POST /api/payment/yookassa/
Content-Type: application/json

{
    "event": "payment.succeeded",
    "object": {
        "id": "payment_id",
        "metadata": {
            "order_id": "order_id"
        }
    }
}
```

**Поддерживаемые события:**
- `payment.succeeded` - платеж успешен
- `payment.canceled` - платеж отменен

## 📝 Примеры использования

### Python (requests)

```python
import requests

# Аутентификация
response = requests.post('http://api.example.com/api/auth/login/', {
    'username': 'your_username',
    'password': 'your_password'
})
token = response.json()['access']

# Создание продукта
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://api.example.com/api/products/', {
    'title': 'New Product',
    'description': 'Product description',
    'price': '99.99'
}, headers=headers)

# Поиск продуктов
response = requests.get('http://api.example.com/api/products/', {
    'search': 'laptop',
    'min_price': '100'
})
products = response.json()['results']
```

### JavaScript (fetch)

```javascript
// Аутентификация
const response = await fetch('http://api.example.com/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: 'your_username',
        password: 'your_password'
    })
});

const { access } = await response.json();

// Создание продукта
const productResponse = await fetch('http://api.example.com/api/products/', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${access}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        title: 'New Product',
        description: 'Product description',
        price: '99.99'
    })
});

// Поиск продуктов
const searchResponse = await fetch('http://api.example.com/api/products/?search=laptop&min_price=100');
const { results: products } = await searchResponse.json();
```

### cURL

```bash
# Аутентификация
curl -X POST http://api.example.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'

# Создание продукта
curl -X POST http://api.example.com/api/products/ \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Product","description":"Description","price":"99.99"}'

# Поиск продуктов
curl "http://api.example.com/api/products/?search=laptop&min_price=100"
```

## 📚 Дополнительные ресурсы

- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [API Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Serializers](https://www.django-rest-framework.org/api-guide/serializers/)

## 🆘 Поддержка

Если у вас есть вопросы по API:

1. Проверьте документацию
2. Создайте Issue в репозитории
3. Обратитесь к примерам кода
4. Проверьте логи сервера

---

Удачи с использованием API! 🚀


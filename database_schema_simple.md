# Упрощенная схема базы данных ReShop

## Основные сущности

```mermaid
graph TD
    A[👤 User<br/>Пользователь] --> B[🛍️ Product<br/>Товар]
    A --> C[📦 Order<br/>Заказ]
    A --> D[💬 ProductComment<br/>Комментарий]
    
    B --> E[🖼️ ProductImage<br/>Изображение]
    B --> C
    B --> D
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fce4ec
```

## Краткое описание

| Таблица | Назначение | Ключевые поля |
|---------|------------|---------------|
| **User** | Пользователи системы | id, email, role, avatar, bio |
| **Product** | Цифровые товары | id, title, price, seller_id |
| **Order** | Заказы покупателей | id, buyer_id, product_id, status |
| **ProductComment** | Отзывы и рейтинги | id, product_id, user_id, rating |
| **ProductImage** | Изображения товаров | id, product_id, image |

## Связи между таблицами

- **User** → **Product** (один ко многим) - продавец создает товары
- **User** → **Order** (один ко многим) - покупатель делает заказы  
- **Product** → **Order** (один ко многим) - товар входит в заказы
- **Product** → **ProductComment** (один ко многим) - товар получает отзывы
- **Product** → **ProductImage** (один ко многим) - товар имеет изображения

## Типы пользователей

- **👨‍💼 Продавец (seller)** - создает товары, получает заказы
- **👤 Покупатель (buyer)** - просматривает товары, делает заказы
- **🔄 Оба** - могут оставлять комментарии и рейтинги

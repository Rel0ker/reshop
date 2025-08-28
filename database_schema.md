# Схема базы данных ReShop

## Обзор системы
ReShop - это цифровая торговая площадка, где пользователи могут покупать и продавать цифровые товары.

## Диаграмма базы данных

```mermaid
erDiagram
    User {
        UUID id PK
        string username
        string email UK
        string role "buyer/seller"
        string first_name
        string last_name
        string bio
        string location
        string phone
        string website
        image avatar
        boolean is_active
        datetime date_joined
        datetime last_login
    }

    Product {
        UUID id PK
        UUID seller_id FK
        string title
        text description
        decimal price
        int quantity
        string download_link
        text usage_instructions
        text seller_info
        string image_url
        datetime created_at
    }

    ProductImage {
        int id PK
        UUID product_id FK
        image image
    }

    Order {
        UUID id PK
        UUID buyer_id FK
        UUID product_id FK
        int quantity
        text comment
        string receipt_email
        string status "pending/paid/delivered/canceled"
        datetime created_at
    }

    ProductComment {
        UUID id PK
        UUID product_id FK
        UUID user_id FK
        text text
        int rating "1-5"
        datetime created_at
        datetime updated_at
    }

    %% Связи между таблицами
    User ||--o{ Product : "продает"
    User ||--o{ Order : "покупает"
    User ||--o{ ProductComment : "оставляет комментарии"
    
    Product ||--o{ ProductImage : "имеет изображения"
    Product ||--o{ Order : "включается в заказы"
    Product ||--o{ ProductComment : "получает комментарии"
    
    Order }o--|| Product : "содержит"
    Order }o--|| User : "принадлежит покупателю"
    
    ProductComment }o--|| Product : "относится к"
    ProductComment }o--|| User : "написан пользователем"
```

## Описание таблиц

### 1. User (Пользователь)
- **Основная таблица** для всех пользователей системы
- **Роли**: покупатель (buyer) или продавец (seller)
- **Профиль**: аватар, биография, местоположение, телефон, веб-сайт
- **Аутентификация**: email как основной идентификатор для входа

### 2. Product (Товар)
- **Цифровые товары** для продажи
- **Связь с продавцом** через Foreign Key
- **Метаданные**: название, описание, цена, количество
- **Цифровое содержимое**: ссылка для скачивания, инструкции по использованию
- **Информация от продавца** и изображения

### 3. ProductImage (Изображения товара)
- **Множественные изображения** для одного товара
- **Загрузка файлов** в папку products/

### 4. Order (Заказ)
- **Связь покупателя с товаром**
- **Статусы заказа**: ожидание оплаты, оплачен, доставлен, отменен
- **Дополнительная информация**: комментарий, email для чека

### 5. ProductComment (Комментарии к товару)
- **Отзывы и рейтинги** от пользователей
- **Рейтинг по шкале 1-5**
- **Временные метки** создания и обновления

## Ключевые особенности архитектуры

✅ **UUID первичные ключи** для безопасности и масштабируемости  
✅ **Гибкая система ролей** (покупатель/продавец)  
✅ **Поддержка множественных изображений** для товаров  
✅ **Система статусов заказов** для отслеживания  
✅ **Система комментариев и рейтингов** для товаров  
✅ **Расширенный профиль пользователя** с дополнительной информацией  

## Технологический стек

- **Backend**: Django (Python)
- **База данных**: SQLite (разработка) / PostgreSQL (продакшн)
- **Файловое хранилище**: Локальная файловая система
- **Frontend**: Vue.js с TypeScript

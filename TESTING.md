# Testing Guide

Руководство по тестированию Reshop - Digital Marketplace.

## 🧪 Обзор

Этот документ описывает стратегию тестирования Reshop, включая:
- Unit тесты для backend
- Component тесты для frontend
- Integration тесты
- E2E тесты
- Performance тесты
- Security тесты

## 🎯 Стратегия тестирования

### Пирамида тестирования

```
    E2E Tests (10%)
       /\
      /  \
Integration Tests (20%)
     /\
    /  \
Unit Tests (70%)
```

### Принципы

1. **Автоматизация** - все тесты должны выполняться автоматически
2. **Быстрота** - unit тесты должны выполняться быстро (< 1 секунды)
3. **Изоляция** - тесты не должны зависеть друг от друга
4. **Повторяемость** - тесты должны давать одинаковый результат
5. **Покрытие** - стремимся к 80%+ покрытию кода

## 🐍 Backend Testing (Django)

### Настройка

```bash
# Установка зависимостей для тестирования
pip install -r requirements-dev.txt

# Создание тестовой базы данных
python manage.py test --keepdb
```

### Структура тестов

```
core/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_serializers.py
│   ├── test_permissions.py
│   └── test_integration.py
```

### Примеры тестов

#### Тестирование моделей

```python
# core/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Product, Order

User = get_user_model()

class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='seller'
        )
        
    def test_product_creation(self):
        product = Product.objects.create(
            title='Test Product',
            description='Test Description',
            price='100.00',
            seller=self.user
        )
        
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.price, '100.00')
        self.assertEqual(product.seller, self.user)
        
    def test_product_str_representation(self):
        product = Product.objects.create(
            title='Test Product',
            description='Test Description',
            price='100.00',
            seller=self.user
        )
        
        self.assertEqual(str(product), 'Test Product')
```

#### Тестирование views

```python
# core/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Product, User

class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='seller'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'title': 'Test Product',
            'description': 'Test Description',
            'price': '100.00'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        
    def test_list_products(self):
        Product.objects.create(
            title='Product 1',
            description='Description 1',
            price='100.00',
            seller=self.user
        )
        Product.objects.create(
            title='Product 2',
            description='Description 2',
            price='200.00',
            seller=self.user
        )
        
        url = reverse('product-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
```

#### Тестирование serializers

```python
# core/tests/test_serializers.py
from django.test import TestCase
from core.serializers import ProductSerializer
from core.models import Product, User

class ProductSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='seller'
        )
        
    def test_product_serializer_valid_data(self):
        data = {
            'title': 'Test Product',
            'description': 'Test Description',
            'price': '100.00'
        }
        
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
    def test_product_serializer_invalid_data(self):
        data = {
            'title': '',  # Пустой заголовок
            'description': 'Test Description',
            'price': 'invalid_price'  # Неверная цена
        }
        
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertIn('price', serializer.errors)
```

#### Тестирование permissions

```python
# core/tests/test_permissions.py
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Product, User
from core.permissions import IsSeller

class IsSellerPermissionTest(APITestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        
    def test_seller_can_create_product(self):
        self.client.force_authenticate(user=self.seller)
        url = reverse('product-list')
        data = {
            'title': 'Test Product',
            'description': 'Test Description',
            'price': '100.00'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_buyer_cannot_create_product(self):
        self.client.force_authenticate(user=self.buyer)
        url = reverse('product-list')
        data = {
            'title': 'Test Product',
            'description': 'Test Description',
            'price': '100.00'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

### Запуск тестов

```bash
# Все тесты
python manage.py test

# Конкретное приложение
python manage.py test core

# Конкретный тест
python manage.py test core.tests.test_models.ProductModelTest

# С покрытием
coverage run --source='.' manage.py test
coverage report
coverage html

# Параллельное выполнение
python manage.py test --parallel
```

## 🎨 Frontend Testing (Vue.js)

### Настройка

```bash
cd frontend-vue

# Установка зависимостей
npm install

# Запуск тестов
npm test

# Запуск тестов в watch режиме
npm run test:watch
```

### Структура тестов

```
frontend-vue/
├── tests/
│   ├── unit/
│   │   ├── components/
│   │   ├── composables/
│   │   └── utils/
│   └── e2e/
```

### Примеры тестов

#### Тестирование компонентов

```typescript
// tests/unit/components/ProductCard.spec.ts
import { mount } from '@vue/test-utils'
import ProductCard from '@/components/ProductCard.vue'

describe('ProductCard', () => {
  const mockProduct = {
    id: '1',
    title: 'Test Product',
    price: '100.00',
    description: 'Test Description',
    images: [{ image: 'test.jpg' }]
  }

  it('renders product information correctly', () => {
    const wrapper = mount(ProductCard, {
      props: { product: mockProduct }
    })

    expect(wrapper.text()).toContain('Test Product')
    expect(wrapper.text()).toContain('100.00')
    expect(wrapper.text()).toContain('Test Description')
  })

  it('emits click event when clicked', async () => {
    const wrapper = mount(ProductCard, {
      props: { product: mockProduct }
    })

    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
```

#### Тестирование composables

```typescript
// tests/unit/composables/useAuth.spec.ts
import { useAuth } from '@/composables/useAuth'
import { createPinia, setActivePinia } from 'pinia'

describe('useAuth', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with default values', () => {
    const auth = useAuth()
    
    expect(auth.user).toBeNull()
    expect(auth.isAuthenticated).toBe(false)
    expect(auth.token).toBeNull()
  })

  it('can login user', async () => {
    const auth = useAuth()
    const mockUser = { id: '1', username: 'testuser' }
    
    await auth.login('testuser', 'password')
    
    expect(auth.user).toEqual(mockUser)
    expect(auth.isAuthenticated).toBe(true)
  })

  it('can logout user', async () => {
    const auth = useAuth()
    
    // Сначала логинимся
    await auth.login('testuser', 'password')
    expect(auth.isAuthenticated).toBe(true)
    
    // Затем выходим
    await auth.logout()
    expect(auth.user).toBeNull()
    expect(auth.isAuthenticated).toBe(false)
  })
})
```

### Запуск тестов

```bash
# Unit тесты
npm run test:unit

# E2E тесты
npm run test:e2e

# Покрытие
npm run test:coverage

# Тесты в watch режиме
npm run test:watch
```

## 🔗 Integration Testing

### API тесты

```python
# core/tests/test_integration.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Product, Order, User

class OrderIntegrationTest(APITestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            title='Test Product',
            description='Test Description',
            price='100.00',
            seller=self.seller
        )
        
    def test_complete_order_flow(self):
        """Тестирование полного процесса заказа"""
        
        # 1. Покупатель авторизуется
        self.client.force_authenticate(user=self.buyer)
        
        # 2. Создается заказ
        order_url = reverse('payment-create')
        order_data = {
            'product': str(self.product.id),
            'quantity': 2,
            'receipt_email': 'buyer@example.com'
        }
        
        order_response = self.client.post(order_url, order_data)
        self.assertEqual(order_response.status_code, status.HTTP_201_CREATED)
        
        # 3. Проверяем, что заказ создан
        order_id = order_response.data['id']
        order = Order.objects.get(id=order_id)
        self.assertEqual(order.buyer, self.buyer)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 2)
        
        # 4. Проверяем статус заказа
        self.assertEqual(order.status, Order.Status.PENDING)
```

### Database тесты

```python
# core/tests/test_database.py
from django.test import TestCase, TransactionTestCase
from django.db import transaction
from core.models import Product, User

class ProductDatabaseTest(TransactionTestCase):
    def test_product_creation_transaction(self):
        """Тестирование транзакций при создании продукта"""
        
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='seller'
        )
        
        # Создаем продукт в транзакции
        with transaction.atomic():
            product = Product.objects.create(
                title='Test Product',
                description='Test Description',
                price='100.00',
                seller=user
            )
            
            # Проверяем, что продукт создан
            self.assertIsNotNone(product.id)
            
        # Проверяем, что продукт сохранен в базе
        saved_product = Product.objects.get(id=product.id)
        self.assertEqual(saved_product.title, 'Test Product')
```

## 🚀 Performance Testing

### Load тесты

```python
# core/tests/test_performance.py
import time
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from core.models import Product, User

class PerformanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='seller'
        )
        
        # Создаем много продуктов для тестирования
        for i in range(100):
            Product.objects.create(
                title=f'Product {i}',
                description=f'Description {i}',
                price=f'{i}.00',
                seller=self.user
            )
        
    def test_product_list_performance(self):
        """Тестирование производительности списка продуктов"""
        
        start_time = time.time()
        
        url = reverse('product-list')
        response = self.client.get(url)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(execution_time, 1.0)  # Менее 1 секунды
        
    def test_product_search_performance(self):
        """Тестирование производительности поиска"""
        
        start_time = time.time()
        
        url = reverse('product-list')
        response = self.client.get(url, {'search': 'Product'})
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(execution_time, 0.5)  # Менее 0.5 секунды
```

### Memory тесты

```python
# core/tests/test_memory.py
import psutil
import os
from django.test import TestCase
from core.models import Product, User

class MemoryTest(TestCase):
    def test_memory_usage(self):
        """Тестирование использования памяти"""
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Создаем много объектов
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='seller'
        )
        
        products = []
        for i in range(1000):
            product = Product.objects.create(
                title=f'Product {i}',
                description=f'Description {i}',
                price=f'{i}.00',
                seller=user
            )
            products.append(product)
        
        # Проверяем использование памяти
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Увеличение памяти должно быть разумным (< 100MB)
        self.assertLess(memory_increase, 100 * 1024 * 1024)
```

## 🔒 Security Testing

### Authentication тесты

```python
# core/tests/test_security.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Product, User

class SecurityTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            title='Test Product',
            description='Test Description',
            price='100.00',
            seller=self.user
        )
        
    def test_unauthorized_access(self):
        """Тестирование доступа без авторизации"""
        
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        
        # Должен быть доступен для чтения
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_unauthorized_modification(self):
        """Тестирование модификации без авторизации"""
        
        url = reverse('product-detail', args=[self.product.id])
        data = {'title': 'Modified Title'}
        response = self.client.put(url, data)
        
        # Должен быть запрещен
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_cross_user_access(self):
        """Тестирование доступа к чужим данным"""
        
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123',
            role='seller'
        )
        
        self.client.force_authenticate(user=other_user)
        url = reverse('product-detail', args=[self.product.id])
        data = {'title': 'Modified Title'}
        response = self.client.put(url, data)
        
        # Должен быть запрещен
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
```

### SQL Injection тесты

```python
# core/tests/test_sql_injection.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Product, User

class SQLInjectionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='seller'
        )
        
    def test_search_sql_injection(self):
        """Тестирование защиты от SQL injection в поиске"""
        
        malicious_inputs = [
            "'; DROP TABLE core_product; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM core_user --",
            "'; INSERT INTO core_product VALUES (999, 'hacked'); --"
        ]
        
        for malicious_input in malicious_inputs:
            url = reverse('product-list')
            response = self.client.get(url, {'search': malicious_input})
            
            # Должен вернуть 200, но не выполнить вредоносный SQL
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Проверяем, что данные не повреждены
            products_count = Product.objects.count()
            self.assertGreaterEqual(products_count, 0)
```

## 📊 Coverage Reports

### Настройка coverage

```ini
# .coveragerc
[run]
source = .
omit = 
    */tests/*
    */migrations/*
    */venv/*
    manage.py
    */settings.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod
```

### Запуск coverage

```bash
# Backend
coverage run --source='.' manage.py test
coverage report
coverage html

# Frontend
npm run test:coverage
```

## 🚨 CI/CD Testing

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        SECRET_KEY: test-secret-key
        DEBUG: True
      run: |
        python manage.py test --verbosity=2 --parallel
        
    - name: Generate coverage report
      run: |
        coverage run --source='.' manage.py test
        coverage report
        coverage xml
        
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## 📚 Best Practices

### 1. Наименование тестов

```python
# Хорошо
def test_user_can_create_product_when_authenticated_as_seller(self):
    pass

def test_product_price_cannot_be_negative(self):
    pass

# Плохо
def test1(self):
    pass

def test_something(self):
    pass
```

### 2. Структура тестов

```python
class ProductTest(TestCase):
    def setUp(self):
        """Подготовка данных для каждого теста"""
        pass
        
    def test_specific_behavior(self):
        """Тестирование конкретного поведения"""
        # Arrange - подготовка
        # Act - действие
        # Assert - проверка
        pass
        
    def tearDown(self):
        """Очистка после каждого теста"""
        pass
```

### 3. Mock и Stub

```python
from unittest.mock import patch, MagicMock

class PaymentTest(TestCase):
    @patch('core.services.yookassa.Payment.create')
    def test_payment_creation(self, mock_payment_create):
        """Тестирование создания платежа с mock"""
        
        # Настройка mock
        mock_payment = MagicMock()
        mock_payment.id = 'test_payment_id'
        mock_payment.confirmation.confirmation_url = 'https://test.com'
        mock_payment_create.return_value = mock_payment
        
        # Тест
        # ...
        
        # Проверка вызова
        mock_payment_create.assert_called_once()
```

## 🆘 Troubleshooting

### Частые проблемы

#### 1. Тесты зависают

```bash
# Проверьте базу данных
python manage.py dbshell

# Очистите кэш
python manage.py flush

# Пересоздайте тестовую базу
python manage.py test --keepdb
```

#### 2. Проблемы с аутентификацией

```python
# Используйте force_authenticate для тестов
self.client.force_authenticate(user=self.user)

# Или создайте токен
from rest_framework_simplejwt.tokens import RefreshToken
token = RefreshToken.for_user(self.user)
self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
```

#### 3. Проблемы с базой данных

```python
# Используйте TransactionTestCase для тестов с базой данных
from django.test import TransactionTestCase

class MyTest(TransactionTestCase):
    def setUp(self):
        # База данных будет очищена перед каждым тестом
        pass
```

## 📚 Дополнительные ресурсы

- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Vue Testing](https://vuejs.org/guide/scaling-up/testing.html)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Coverage.py](https://coverage.readthedocs.io/)

---

Удачи с тестированием! 🧪


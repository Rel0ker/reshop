"""
Модели: Пользователь (покупатель/продавец), Цифровой товар, Заказ
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Расширяем стандартного User, добавляя роль.
    """
    class Roles(models.TextChoices):
        BUYER = "buyer", "Покупатель"
        SELLER = "seller", "Продавец"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=6, choices=Roles.choices)

    # email вместо username для логина
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]        # username всё ещё обязателен внутри Django

    email = models.EmailField(unique=True)


class Product(models.Model):
    """
    Цифровой товар, привязан к продавцу (seller).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    download_link = models.URLField(blank=True)
    usage_instructions = models.TextField(blank=True, verbose_name="Инструкция по использованию")
    seller_info = models.TextField(blank=True, verbose_name="Информация от продавца")
    image_url = models.URLField(blank=True, verbose_name="URL изображения товара")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """
    Изображение для товара. У одного товара может быть несколько.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.title}"


class Order(models.Model):
    """
    Заказ = связь покупателя с конкретным товаром.
    """
    class Status(models.TextChoices):
        PENDING = "pending", "В ожидании оплаты"
        PAID = "paid", "Оплачен"
        DELIVERED = "delivered", "Доставлен"
        CANCELED = "canceled", "Отменен"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True)
    receipt_email = models.EmailField(blank=True, null=True)
    status = models.CharField(
        max_length=9, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.title}"


class ProductComment(models.Model):
    """
    Комментарий к товару от пользователя.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_comments')
    text = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий к товару'
        verbose_name_plural = 'Комментарии к товарам'

    def __str__(self):
        return f"Comment by {self.user.email} on {self.product.title}"

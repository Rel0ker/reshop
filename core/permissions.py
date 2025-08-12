"""
Кастомные permissions: только продавец может создавать товары и
только покупатель – заказы.
"""
from rest_framework import permissions


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "seller"


class IsBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "buyer"


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.role == "seller"


class IsOrderOwnerOrSeller(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "seller":
            return obj.product.seller == request.user
        return obj.buyer == request.user


class HasPurchasedProduct(permissions.BasePermission):
    """
    Разрешает доступ только пользователям, которые купили товар.
    """
    def has_permission(self, request, view):
        if request.method not in ['POST', 'PUT', 'PATCH']:
            return True
        
        # Для создания/редактирования комментария проверяем, что пользователь купил товар
        if request.method == 'POST':
            product_id = request.data.get('product')
            if not product_id:
                return False
            
            # Проверяем, есть ли у пользователя оплаченный заказ на этот товар
            from .models import Order
            return Order.objects.filter(
                buyer=request.user,
                product_id=product_id,
                status__in=['paid', 'delivered']
            ).exists()
        
        return True

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterViewSet, 
    ProductViewSet, 
    OrderViewSet, 
    UserViewSet, 
    PaymentViewSet, 
    PaymentWebhookViewSet,
    ProductCommentViewSet
)

router = DefaultRouter()
router.register(r'auth/register', RegisterViewSet, basename='register')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'users', UserViewSet, basename='user')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'payments/webhook', PaymentWebhookViewSet, basename='payment-webhook')
router.register(r'comments', ProductCommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
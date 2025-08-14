from rest_framework import viewsets, mixins, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Product, Order, ProductComment, User, ProductImage
from .serializers import (
    RegisterSerializer,
    ProductSerializer,
    OrderSerializer,
    OrderCreateSerializer,
    UserSerializer,
    ProductCommentSerializer,
    TokenObtainPairSerializer as CustomTokenObtainPairSerializer,
    LoginResponseSerializer,
)
from .permissions import IsSeller, IsBuyer, IsSellerOrReadOnly, IsOrderOwnerOrSeller, HasPurchasedProduct

from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View


class CustomLoginView(TokenObtainPairView):
    """
    Кастомный эндпоинт логина который возвращает токен и информацию о пользователе
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        # Сначала валидируем данные
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Получаем пользователя из валидированных данных
        user = serializer.user
        
        # Вызываем родительский метод для получения токенов
        response = super().post(request, *args, **kwargs)
        
        # Создаем ответ с пользователем
        response_data = {
            'access': response.data['access'],
            'refresh': response.data['refresh'],
            'user': UserSerializer(user).data
        }
        return Response(response_data)


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    POST /api/auth/register
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProductPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    """
    /api/products/…
    """
    print("🔥 PRODUCT VIEWSET LOADED WITH NEW CODE! 🔥")
    
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']

    def list(self, request, *args, **kwargs):
        """
        Переопределяем list чтобы передавать request в контекст сериализатора
        и добавляем кастомный поиск
        """
        # Получаем базовый queryset
        queryset = self.get_queryset()
        
        # Кастомный поиск если передан параметр search
        search_query = request.query_params.get('search', None)
        if search_query:
            # Экранируем специальные символы для iregex
            import re
            escaped_query = re.escape(search_query)
            
            # Используем iregex который работает лучше чем icontains
            from django.db.models import Q
            
            # Поиск по названию и описанию с использованием iregex
            queryset = queryset.filter(
                Q(title__iregex=escaped_query) | 
                Q(description__iregex=escaped_query)
            )
        
        # Пагинация
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_custom_search(self, queryset, search_query):
        """
        Кастомный поиск по названию и описанию товара
        """
        from django.db.models import Q
        import logging
        
        logger = logging.getLogger(__name__)
        logger.info(f"🔍 Performing custom search for: '{search_query}'")
        logger.info(f"🔍 Initial queryset count: {queryset.count()}")
        
        # Создаем Q объекты для поиска
        title_search = Q(title__icontains=search_query)
        description_search = Q(description__icontains=search_query)
        
        # Объединяем поиск по названию и описанию
        filtered_queryset = queryset.filter(title_search | description_search)
        
        logger.info(f"🔍 Filtered queryset count: {filtered_queryset.count()}")
        logger.info(f"🔍 Search query: {search_query}")
        
        return filtered_queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Переопределяем retrieve чтобы передавать request в контекст сериализатора
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info("=" * 50)
        logger.info("PRODUCT UPDATE STARTED")
        logger.info("=" * 50)
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request content type: {request.content_type}")
        logger.info(f"Request data: {request.data}")
        logger.info(f"Request FILES: {request.FILES}")
        logger.info(f"Request user: {request.user}")
        logger.info(f"Product ID: {kwargs.get('pk')}")
        logger.info("=" * 50)
        
        # Также выводим в консоль для отладки
        print("=" * 50)
        print("PRODUCT UPDATE STARTED")
        print("=" * 50)
        print(f"Request method: {request.method}")
        print(f"Request content type: {request.content_type}")
        print(f"Request data: {request.data}")
        print(f"Request FILES: {request.FILES}")
        print(f"Request user: {request.user}")
        print(f"Product ID: {kwargs.get('pk')}")
        print("=" * 50)
        
        try:
            instance = self.get_object()
            logger.info(f"Product instance found: {instance.id}")
            print(f"Product instance found: {instance.id}")
            
            serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
            logger.info(f"Update serializer created: {serializer}")
            print(f"Update serializer created: {serializer}")
            
            if not serializer.is_valid():
                logger.error(f"Update serializer validation errors: {serializer.errors}")
                print(f"Update serializer validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            logger.info("Update serializer is valid, proceeding to save...")
            print("Update serializer is valid, proceeding to save...")
            
            # Сохраняем товар
            updated_product = serializer.save()
            logger.info(f"Product updated successfully: {updated_product.id}")
            print(f"Product updated successfully: {updated_product.id}")
            
            # Обрабатываем новые изображения
            if 'uploaded_images' in request.FILES:
                logger.info(f"Processing {len(request.FILES.getlist('uploaded_images'))} new images")
                print(f"Processing {len(request.FILES.getlist('uploaded_images'))} new images")
                
                for uploaded_file in request.FILES.getlist('uploaded_images'):
                    logger.info(f"Creating ProductImage for file: {uploaded_file.name}")
                    print(f"Creating ProductImage for file: {uploaded_file.name}")
                    
                    ProductImage.objects.create(
                        product=updated_product,
                        image=uploaded_file
                    )
                    logger.info(f"ProductImage created for: {uploaded_file.name}")
                    print(f"ProductImage created for: {uploaded_file.name}")
            
            # Обрабатываем удаление изображений
            if 'images_to_delete' in request.data:
                images_to_delete = request.data.getlist('images_to_delete')
                logger.info(f"Deleting {len(images_to_delete)} images: {images_to_delete}")
                print(f"Deleting {len(images_to_delete)} images: {images_to_delete}")
                
                for image_id in images_to_delete:
                    try:
                        image = ProductImage.objects.get(id=image_id, product=updated_product)
                        image.delete()
                        logger.info(f"Image {image_id} deleted successfully")
                        print(f"Image {image_id} deleted successfully")
                    except ProductImage.DoesNotExist:
                        logger.warning(f"Image {image_id} not found for deletion")
                        print(f"Image {image_id} not found for deletion")
            
            # Получаем обновленные данные с изображениями
            final_serializer = self.get_serializer(updated_product, context={'request': request})
            logger.info("=" * 50)
            logger.info("PRODUCT UPDATE COMPLETED SUCCESSFULLY")
            logger.info("=" * 50)
            print("=" * 50)
            print("PRODUCT UPDATE COMPLETED SUCCESSFULLY")
            print("=" * 50)
            
            # Логируем финальные данные для отладки
            final_data = final_serializer.data
            logger.info(f"Final serializer data: {final_data}")
            logger.info(f"Final images count: {len(final_data.get('images', []))}")
            if final_data.get('images'):
                for i, img in enumerate(final_data['images']):
                    logger.info(f"Final image {i+1}: {img}")
            print(f"Final serializer data: {final_data}")
            print(f"Final images count: {len(final_data.get('images', []))}")
            if final_data.get('images'):
                for i, img in enumerate(final_data['images']):
                    print(f"Final image {i+1}: {img}")
            
            return Response(final_data)
            
        except Exception as e:
            logger.error(f"ERROR updating product: {e}")
            print(f"ERROR updating product: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response(
                {"error": f"Failed to update product: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsSeller])
    def mine(self, request):
        """
        Возвращает ВСЕ товары для текущего аутентифицированного продавца,
        отключая пагинацию для этого эндпоинта.
        """
        user_products = Product.objects.filter(seller=request.user).order_by('-created_at')
        serializer = self.get_serializer(user_products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def has_purchased(self, request, pk=None):
        """
        Проверяет, купил ли текущий пользователь этот товар
        """
        product = self.get_object()
        user = request.user
        
        # Проверяем, есть ли у пользователя оплаченный заказ на этот товар
        has_purchased = Order.objects.filter(
            buyer=user,
            product=product,
            status__in=['paid', 'delivered']
        ).exists()
        
        return Response({
            'has_purchased': has_purchased,
            'product_id': str(product.id)
        })

    def perform_create(self, serializer):
        """
        Продавец-создатель → seller.
        """
        serializer.save(seller=self.request.user)

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsSeller()]
        return [AllowAny()]

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def test_logging(self, request):
        """
        Тестовый endpoint для проверки логирования
        """
        logger.info("TEST LOGGING ENDPOINT CALLED")
        print("TEST LOGGING ENDPOINT CALLED")
        return Response({"message": "Logging test successful", "timestamp": str(datetime.now())})

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def test_search(self, request):
        """
        Тестовый endpoint для проверки поиска
        """
        search_query = request.query_params.get('search', '')
        print(f"🔍 Test search called with query: '{search_query}'")
        
        # Получаем все товары
        all_products = Product.objects.all()
        print(f"🔍 Total products: {all_products.count()}")
        
        # Показываем все названия товаров
        all_titles = [p.title for p in all_products[:5]]  # Первые 5
        print(f"🔍 Sample titles: {all_titles}")
        
        # Пробуем поиск
        if search_query:
            from django.db.models import Q
            
            # Тест 1: icontains
            icontains_result = all_products.filter(title__icontains=search_query)
            print(f"🔍 icontains result count: {icontains_result.count()}")
            
            # Тест 2: iregex
            iregex_result = all_products.filter(title__iregex=search_query)
            print(f"🔍 iregex result count: {iregex_result.count()}")
            
            # Тест 3: contains
            contains_result = all_products.filter(title__contains=search_query)
            print(f"🔍 contains result count: {contains_result.count()}")
            
            # Тест 4: exact
            exact_result = all_products.filter(title__exact=search_query)
            print(f"🔍 exact result count: {exact_result.count()}")
            
            # Тест 5: iexact
            iexact_result = all_products.filter(title__iexact=search_query)
            print(f"🔍 iexact result count: {iexact_result.count()}")
            
            # Показываем названия найденных товаров
            found_titles = [p.title for p in icontains_result]
            print(f"🔍 Found titles (icontains): {found_titles}")
            
            return Response({
                "search_query": search_query,
                "total_products": all_products.count(),
                "icontains_count": icontains_result.count(),
                "iregex_count": iregex_result.count(),
                "contains_count": contains_result.count(),
                "exact_count": exact_result.count(),
                "iexact_count": iexact_result.count(),
                "found_titles": found_titles,
                "sample_titles": all_titles
            })
        
        return Response({"message": "No search query provided", "total_products": all_products.count()})


class ProductCommentViewSet(viewsets.ModelViewSet):
    """
    /api/comments/…
    """
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
    permission_classes = [permissions.IsAuthenticated, HasPurchasedProduct]

    def get_queryset(self):
        """
        Фильтруем комментарии по товару если передан product_id
        """
        queryset = ProductComment.objects.all()
        product_id = self.request.query_params.get('product_id', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """
        Автор комментария → user.
        """
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            # Только автор комментария может редактировать/удалять
            return [permissions.IsAuthenticated()]
        elif self.action in ("create", "list"):
            # Для создания комментария нужна покупка товара, для просмотра - только аутентификация
            return [permissions.IsAuthenticated(), HasPurchasedProduct()]
        return [permissions.IsAuthenticated()]


class OrderViewSet(viewsets.ModelViewSet):
    """
    Покупатель создаёт заказ, а также может получить список своих заказов.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "seller":
            return Order.objects.filter(product__seller=user)
        return Order.objects.filter(buyer=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Переопределяем create для правильной обработки заказов
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Возвращаем полные данные заказа
        from .serializers import OrderSerializer
        full_serializer = OrderSerializer(order, context={'request': request})
        
        # Добавляем базовую информацию о заказе
        response_data = full_serializer.data
        response_data.update({
            'order_created': True,
            'message': 'Заказ успешно создан'
        })
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        """
        Возвращает заказы для текущего аутентифицированного пользователя
        """
        user = request.user
        if user.role == "seller":
            # Для продавца - заказы на его товары
            orders = Order.objects.filter(product__seller=user).order_by('-created_at')
        else:
            # Для покупателя - его заказы
            orders = Order.objects.filter(buyer=user).order_by('-created_at')
        
        serializer = self.get_serializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def confirm(self, request, pk=None):
        """
        Продавец подтверждает заказ (меняет статус на 'paid')
        """
        try:
            order = self.get_object()
            
            # Проверяем, что пользователь является продавцом этого товара
            if request.user.role != "seller" or order.product.seller != request.user:
                return Response(
                    {"error": "У вас нет прав для подтверждения этого заказа"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Проверяем, что заказ в статусе "pending"
            if order.status != "pending":
                return Response(
                    {"error": "Можно подтверждать только заказы в ожидании оплаты"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order.status = "paid"
            order.save()
            
            serializer = self.get_serializer(order)
            return Response(serializer.data)
            
        except Order.DoesNotExist:
            return Response(
                {"error": "Заказ не найден"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        """
        Продавец отклоняет заказ (меняет статус на 'seller_rejected')
        """
        try:
            order = self.get_object()
            
            # Проверяем, что пользователь является продавцом этого товара
            if request.user.role != "seller" or order.product.seller != request.user:
                return Response(
                    {"error": "У вас нет прав для отклонения этого заказа"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Проверяем, что заказ в статусе "pending"
            if order.status != "pending":
                return Response(
                    {"error": "Можно отклонять только заказы в ожидании оплаты"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order.status = "seller_rejected"
            order.save()
            
            serializer = self.get_serializer(order)
            return Response(serializer.data)
            
        except Order.DoesNotExist:
            return Response(
                {"error": "Заказ не найден"}, 
                status=status.HTTP_404_NOT_FOUND
            )


import requests
from django.conf import settings
import uuid
from yookassa.payment import Payment
import logging
from datetime import datetime

# Настраиваем логирование
logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    



class PaymentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Инициализируем Yookassa
        try:
            from django.conf import settings
            from yookassa import Configuration
            
            shop_id = getattr(settings, 'YOOKASSA_SHOP_ID', 'your_shop_id')
            secret_key = getattr(settings, 'YOOKASSA_SECRET_KEY', 'your_secret_key')
            
            logger.info("Initializing Yookassa...")
            logger.info(f"Shop ID configured: {'*' * len(shop_id) if shop_id != 'your_shop_id' else 'NOT SET'}")
            logger.info(f"Secret Key configured: {'*' * len(secret_key) if secret_key != 'your_secret_key' else 'NOT SET'}")
            
            Configuration.account_id = shop_id
            Configuration.secret_key = secret_key
            
            logger.info("Yookassa initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Yookassa: {e}")
            import traceback
            logger.error(f"Initialization traceback: {traceback.format_exc()}")

    def create(self, request, *args, **kwargs):
        logger.info("=" * 50)
        logger.info("PAYMENT ORDER CREATION STARTED")
        logger.info("=" * 50)
        logger.info(f"Request method: {request.method}")
        logger.info("Request data received")
        logger.info(f"Request user: {request.user.username}")
        logger.info("=" * 50)
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        if not serializer.is_valid():
            logger.error(f"Serializer validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Создаем заказ
            order = serializer.save()
            logger.info(f"Order created successfully with ID: {order.id}")
            
            # Создаем платеж в Yookassa
            try:
                logger.info("Starting Yookassa payment creation...")
                
                # Получаем данные для платежа
                amount = float(order.product.price) * order.quantity
                description = f"Заказ {order.id} - {order.product.title}"
                
                logger.info(f"Payment data - Amount: {amount}, Description: {description}")
                
                # Проверяем, что Yookassa инициализирован
                from yookassa import Configuration
                logger.info("Checking Yookassa configuration...")
                
                if not Configuration.account_id or not Configuration.secret_key:
                    raise Exception("Yookassa not properly initialized")
                
                # Создаем платеж
                payment_data = {
                    "amount": {
                        "value": str(amount),
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": f"http://localhost:8000/success/{order.id}/"
                    },
                    "capture": True,
                    "description": description,
                    "metadata": {
                        "order_id": str(order.id),
                        "user_id": str(request.user.id)
                    }
                }
                
                logger.info("Creating Yookassa payment...")
                
                payment = Payment.create(payment_data, idempotency_key=str(order.id))
                
                logger.info(f"Yookassa payment created successfully: {payment.id}")
                logger.info("Payment confirmation URL generated")
                
                # Добавляем информацию о платеже к объекту заказа
                order.payment_id = payment.id
                order.payment_url = payment.confirmation.confirmation_url
                order.amount = amount
                order.currency = 'RUB'
                
                # Возвращаем данные заказа с информацией о платеже
                from .serializers import OrderSerializer
                full_serializer = OrderSerializer(order, context={'request': request})
                
                response_data = full_serializer.data
                response_data.update({
                    'payment_id': payment.id,
                    'payment_url': payment.confirmation.confirmation_url,
                    'amount': amount,
                    'currency': 'RUB',
                    'payment_status': 'pending'
                })
                
                logger.info("Payment response prepared successfully")
                return Response(response_data, status=status.HTTP_201_CREATED)
                
            except Exception as payment_error:
                logger.error(f"ERROR creating Yookassa payment: {payment_error}")
                import traceback
                logger.error(f"Payment traceback: {traceback.format_exc()}")
                
                # Если не удалось создать платеж, возвращаем заказ без платежа
                from .serializers import OrderSerializer
                full_serializer = OrderSerializer(order, context={'request': request})
                
                response_data = full_serializer.data
                response_data.update({
                    'payment_error': str(payment_error),
                    'order_created': True,
                    'payment_status': 'failed'
                })
                
                logger.info("Fallback response prepared (payment failed)")
                return Response(response_data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            logger.error(f"ERROR creating order: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return Response(
                {"error": f"Failed to create order: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentWebhookViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='yookassa')
    def yookassa_webhook(self, request):
        try:
            notification_data = request.data
            print(f"Received Yookassa webhook: {notification_data}")

            if notification_data['event'] == 'payment.succeeded':
                payment_id = notification_data['object']['id']
                order_id = notification_data['object']['metadata']['order_id']
                
                try:
                    order = Order.objects.get(id=order_id)
                    order.status = Order.Status.PAID
                    order.save()
                    print(f"Order {order_id} status updated to PAID.")
                except Order.DoesNotExist:
                    print(f"Order with ID {order_id} not found.")

            elif notification_data['event'] == 'payment.canceled':
                payment_id = notification_data['object']['id']
                order_id = notification_data['object']['metadata']['order_id']

                try:
                    order = Order.objects.get(id=order_id)
                    order.status = Order.Status.CANCELED
                    order.save()
                    print(f"Order {order_id} status updated to CANCELED.")
                except Order.DoesNotExist:
                    print(f"Order with ID {order_id} not found.")

            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error processing Yookassa webhook: {e}")
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderSuccessRedirectView(View):
    """
    Перенаправляет пользователя на frontend страницу успешной оплаты
    """
    def get(self, request, order_id):
        # Перенаправляем на frontend страницу успешной оплаты
        frontend_url = f"http://localhost:5173/order-success/{order_id}"
        return redirect(frontend_url)





class TelegramAuthViewSet(viewsets.ViewSet):
    """
    Авторизация через Telegram
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'], url_path='login')
    def telegram_login(self, request):
        """
        Авторизация через Telegram
        """
        try:
            telegram_data = request.data
            logger.info(f"Telegram auth request received: {telegram_data}")
            
            # Проверяем данные от Telegram
            verified_data = telegram_auth_service.verify_telegram_data(telegram_data)
            if not verified_data:
                return Response(
                    {'error': 'Invalid Telegram data'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Получаем или создаем пользователя
            user = telegram_auth_service.get_or_create_user(verified_data)
            if not user:
                return Response(
                    {'error': 'Failed to create/get user'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Генерируем JWT токены
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            
            # Отправляем уведомление в Telegram
            telegram_auth_service.send_auth_success_message(
                verified_data['telegram_id'], 
                user.username
            )
            
            # Возвращаем токены и информацию о пользователе
            response_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }
            
            logger.info(f"Telegram auth successful for user: {user.username}")
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in Telegram auth: {e}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

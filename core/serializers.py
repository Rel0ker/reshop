"""
Преобразуют модели ⇄ JSON.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Product, Order, ProductImage, ProductComment
import logging

# Настраиваем логирование
logger = logging.getLogger(__name__)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Используется для чтения профиля, не для регистрации.
    """
    avatar = serializers.ImageField(read_only=True)
    class Meta:
        model = User
        fields = ("id", "email", "role", "avatar")


class RegisterSerializer(serializers.ModelSerializer):
    """
    Создание пользователя + хеширование пароля.
    """
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)  # делаем необязательным, так как генерируем из email

    class Meta:
        model = User
        fields = ("id", "email", "username", "password", "role")

    def create(self, validated_data):
        # Если username не предоставлен, генерируем его из email
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email'].split('@')[0]
        
        user = User.objects.create_user(**validated_data)
        return user


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            # Формируем полный URL для изображения
            request = self.context.get('request')
            if request:
                full_url = request.build_absolute_uri(instance.image.url)
                representation['image'] = full_url
                print(f"🖼️ ProductImageSerializer: Built full URL: {full_url}")
                print(f"🖼️ ProductImageSerializer: Original URL: {instance.image.url}")
            else:
                representation['image'] = instance.image.url
                print(f"⚠️ ProductImageSerializer: No request context, using original URL: {instance.image.url}")
        else:
            print(f"⚠️ ProductImageSerializer: No image field for instance {instance.id}")
        return representation


class ProductCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProductComment
        fields = ('id', 'user', 'text', 'rating', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    print("🎨 PRODUCT SERIALIZER LOADED WITH NEW CODE! 🎨")
    
    seller = UserSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    comments = ProductCommentSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = ('id', 'seller', 'title', 'description', 'price', 'quantity', 'download_link', 'usage_instructions', 'seller_info', 'image_url', 'created_at', 'images', 'comments', 'uploaded_images')
        read_only_fields = ("id", "seller", "created_at", "images", "comments")

    def create(self, validated_data):
        logger.info("=" * 50)
        logger.info("PRODUCT SERIALIZER CREATE METHOD")
        logger.info("=" * 50)
        logger.info(f"Validated data: {validated_data}")
        logger.info(f"Validated data keys: {list(validated_data.keys())}")
        
        # Также выводим в консоль
        print("=" * 50)
        print("PRODUCT SERIALIZER CREATE METHOD")
        print("=" * 50)
        print(f"Validated data: {validated_data}")
        print(f"Validated data keys: {list(validated_data.keys())}")
        
        uploaded_images = validated_data.pop("uploaded_images", [])
        logger.info(f"Uploaded images count: {len(uploaded_images)}")
        logger.info(f"Uploaded images: {uploaded_images}")
        print(f"Uploaded images count: {len(uploaded_images)}")
        print(f"Uploaded images: {uploaded_images}")
        
        logger.info("Creating product...")
        print("Creating product...")
        product = super().create(validated_data)
        logger.info(f"Product created with ID: {product.id}")
        print(f"Product created with ID: {product.id}")
        
        if uploaded_images:
            logger.info("Creating ProductImage objects...")
            print("Creating ProductImage objects...")
            for i, image in enumerate(uploaded_images):
                logger.info(f"Processing image {i+1}: {image}")
                logger.info(f"Image type: {type(image)}")
                logger.info(f"Image name: {getattr(image, 'name', 'N/A')}")
                logger.info(f"Image size: {getattr(image, 'size', 'N/A')}")
                
                print(f"Processing image {i+1}: {image}")
                print(f"Image type: {type(image)}")
                print(f"Image name: {getattr(image, 'name', 'N/A')}")
                print(f"Image size: {getattr(image, 'size', 'N/A')}")
                
                try:
                    ProductImage.objects.create(product=product, image=image)
                    logger.info(f"ProductImage {i+1} created successfully")
                    print(f"ProductImage {i+1} created successfully")
                except Exception as e:
                    logger.error(f"ERROR creating ProductImage {i+1}: {e}")
                    print(f"ERROR creating ProductImage {i+1}: {e}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    print(f"Traceback: {traceback.format_exc()}")
        else:
            logger.info("No images to process")
            print("No images to process")
        
        logger.info("=" * 50)
        print("=" * 50)
        return product


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'seller_info', 'image_url')


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_amount = serializers.SerializerMethodField()
    payment_info = serializers.SerializerMethodField()

    def get_total_amount(self, obj):
        return float(obj.product.price) * obj.quantity

    def get_payment_info(self, obj):
        """
        Возвращает информацию о платеже, если она есть в контексте
        """
        if hasattr(obj, 'payment_id'):
            payment_info = {
                'payment_id': getattr(obj, 'payment_id', None),
                'payment_url': getattr(obj, 'payment_url', None),
                'amount': getattr(obj, 'amount', None),
                'currency': getattr(obj, 'currency', None),
                'payment_status': getattr(obj, 'payment_status', None)
            }
            return payment_info
        else:
            return None

    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'comment', 'receipt_email', 'buyer', 'status', 'created_at', 'total_amount', 'payment_info']
        read_only_fields = ("id", "buyer", "status", "created_at")

    def to_representation(self, instance):
        """
        Переопределяем представление для корректного отображения
        """
        representation = super().to_representation(instance)
        
        # Добавляем информацию о покупателе
        if instance.buyer:
            representation['buyer'] = {
                'id': str(instance.buyer.id),
                'email': instance.buyer.email,
                'username': instance.buyer.username
            }
        
        # Убеждаемся, что product правильно сериализуется
        if instance.product:
            representation['product'] = ProductSerializer(instance.product, context=self.context).data
        
        # Добавляем информацию о платеже
        payment_info = self.get_payment_info(instance)
        if payment_info:
            representation['payment_info'] = payment_info
        
        return representation


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания заказов - позволяет записывать product_id
    """
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'comment', 'receipt_email']
        read_only_fields = ("id", "buyer", "status", "created_at")

    def validate_product(self, value):
        """
        Проверяем, что товар существует и доступен для покупки
        """
        if not value:
            raise serializers.ValidationError("Товар обязателен")
        
        if value.quantity <= 0:
            raise serializers.ValidationError("Товар недоступен для покупки")
        
        return value

    def validate(self, data):
        """
        Дополнительная валидация
        """
        if data.get('quantity', 0) <= 0:
            raise serializers.ValidationError("Количество должно быть больше 0")
        
        return data

    def to_representation(self, instance):
        """
        Переопределяем представление для корректного отображения
        """
        # Импортируем здесь чтобы избежать циклических импортов
        from .serializers import OrderSerializer
        return OrderSerializer(instance, context=self.context).data

    def create(self, validated_data):
        """
        Создаем заказ с текущим пользователем как покупателем
        """
        # Получаем пользователя из контекста
        buyer = self.context['request'].user
        
        # Создаем заказ
        order = Order.objects.create(
            buyer=buyer,
            product=validated_data['product'],
            quantity=validated_data['quantity'],
            comment=validated_data.get('comment', ''),
            receipt_email=validated_data.get('receipt_email', ''),
            status=Order.Status.PENDING
        )
        
        return order


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Добавляем роль в токен
        token['role'] = user.role
        return token


class LoginResponseSerializer(serializers.Serializer):
    """
    Сериализатор для ответа при логине
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()

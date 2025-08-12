from django.contrib import admin
from .models import Product, Order, ProductImage, User, ProductComment

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ("title", "price", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True

class ProductCommentInline(admin.TabularInline):
    model = ProductComment
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = ("user", "text", "rating", "created_at")

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductCommentInline]
    list_display = ("title", "seller", "price", "created_at")
    search_fields = ("title", "description")
    list_filter = ("seller",)

class UserAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = ("email", "role", "is_active", "is_staff")
    search_fields = ("email", "username")
    list_filter = ("role", "is_active", "is_staff")

class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("text", "user__email", "product__title")
    readonly_fields = ("created_at", "updated_at")

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(ProductImage)
admin.site.register(User, UserAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)

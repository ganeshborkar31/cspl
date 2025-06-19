from django.contrib import admin
from .models import CustomUser, CustomUserRole, ExpireToken, OTP, Product, Category, Order, OrderItem, Payment


@admin.register(CustomUser)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'is_active')
    search_fields = ('first_name',)  
    ordering = ('first_name',)
    # filter_horizontal = ('is_active',)   many to maany filed 
    # filter_verticle = ("is_active", )
    list_filter = ('is_active',)

@admin.register(CustomUserRole)
class CustomUserRole(admin.ModelAdmin):
    list_display = ('name' ,'description')
    search_fields = ('name',) 
    ordering = ('name',)
    list_filter = ('name',)
    
@admin.register(ExpireToken)
class ExpireTokenAdmin(admin.ModelAdmin):
    list_display = ('key' ,'user', 'created', 'expire')
    search_fields = ('user',) 
    ordering = ('user',)
    
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('email' ,'otp', 'expire', "is_verified")
    search_fields = ('email',) 
    ordering = ('email',)
    list_filter = ('is_verified',)
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'tag', 'is_active')
    list_filter = ('is_active',)
    ordering = ('name',)
    search_fields = ('name',)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    list_filter = ('is_active',)
    ordering = ('name',)
    search_fields = ('name',) 
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status')
    search_fields = ('customer__username', 'id')
    list_filter = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_filter = ('product',)
    ordering = ('order',)
    search_fields = ('product__name', 'order__id')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'payment_mode', 'status', 'payment_date', 'transaction_id')
    list_filter = ('status', 'payment_mode', 'payment_date')
    ordering = ('-payment_date',)
    search_fields = ('order__id', 'transaction_id')
    
    
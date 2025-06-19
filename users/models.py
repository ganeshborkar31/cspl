from django.db import models

from django.contrib.auth.models import  Group, User, AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from  django.utils.translation import gettext_lazy as _



class CustomUser(User):
    phone_number = models.CharField(max_length = 15, unique=True, blank = True, null = True)
    
    def __str__(self):
        return self.username

    def clean(self, *args, **kwargs):
        try:
            email_exist = CustomUser.objects.get(email=self.email)
        except CustomUser.DoesNotExist:
            email_exist = None
        
        if email_exist:
            raise ValidationError({'email':_('Email is Already Exist')})  
        
    
    # def save(self, *args, **kwargs):

    #     if CustomUser.objects.filter(email=self.email).exists():
    #         raise ValidationError("Email is already Exist.")
        
    #     super().save(*args, **kwargs)
        
    
class CustomUserRole(Group):
    description = models.TextField(blank = True, null = True, default = '')  
 
    def __str__(self):
        return self.name
    

class ExpireToken(Token):
    # created = models.DateTimeField(auto_now_add=True)
    expire = models.DateTimeField(default = timezone.now() + timedelta(minutes = 5))
    
    def is_expire(self):
        return timezone.now() > self.expire
    
class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length = 6)
    expire = models.DateTimeField(default = timezone.now() + timedelta(minutes = 5))
    is_verified = models.BooleanField(default = False)
    
    def is_expire(self):
        return timezone.now() > self.expire
    
    
    
class Category(models.Model):  
    
    name = models.CharField(max_length = 50, null = False, unique = True)
    description =  models.TextField(null = True)
    is_active = models.BooleanField(default = True)

    
class Product(models.Model):  
     
    TAG_CHOICES = (
    ("VEG", "Veg"),
    ("NON-VEG", "Non-Veg"),
    )

    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    name = models.CharField(max_length = 50, null = False, unique = True)
    description =  models.TextField(null = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    tag = models.CharField(max_length = 20, choices = TAG_CHOICES)
    is_active = models.BooleanField(default = True)
    
class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )

    customer = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    order_date = models.DateTimeField(auto_now_add = True)
    total_amount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default="PENDING")
    # created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)  

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Payment(models.Model):
    PAYMENT_STATUS = (
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    )
    
    PAYMENT_MODE = (
        ("ONLINE", "Online"),
        ("CASH", 'Cash'),
    )

    order = models.OneToOneField(Order, on_delete = models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add = True)
    amount = models.DecimalField(max_digits = 10, decimal_places=2)
    status = models.CharField(max_length = 20, choices = PAYMENT_STATUS, default="PENDING")
    payment_mode = models.CharField(max_length = 10, choices = PAYMENT_MODE, default="Cash")
    transaction_id = models.CharField(max_length = 100, blank = True, null = True)
    

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.status}"
    
    
    




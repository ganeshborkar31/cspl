# serializers.py
from rest_framework import serializers
from .models import CustomUserRole, Product, Category

class CustomUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserRole
        fields = ['id', 'name', 'description']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'tag', 'is_active', 'category', 'category_id']

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Category, Product

@receiver(post_save, sender = Category)
def deactivate_products_if_category_inactive(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    try:
        previous = Category.objects.get(pk = instance.pk)
        
    except Category.DoesNotExist:
        return
    
    if previous.is_active and not instance.is_active:
        Product.objects.filter(category = instance).update(is_active = False)
        

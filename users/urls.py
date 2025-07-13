from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

# from .views import (login, get_users, send_mail, register,verify_mail, place_order, make_payment, 
#                     download_products_excel,upload_products_excel, update_user, delete_user, list_groups_with_users, view_orders_paginated, 
#                     CustomUserRoleAPIView, ProductViewSet)

from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('login/', login, name = 'login'),
    path('users/', get_users, name = "get_users"),
    path('send-mail/', send_mail, name = "send_mail"),
    path('verify-mail/', verify_mail, name = "verify_mail"),
    path('register/', register, name = "regiser_user"),
    path('update/', update_user, name = "update_user"),
    path('delete/', delete_user, name = "delete_user"),
    path('groups-users/', list_groups_with_users, name = "get_groups_and_users"),
    path('place-order/', place_order, name = "place_order"),
    path('make-payment/', make_payment, name = "make_payemnt"),
    path('orders/', view_orders_paginated, name = "view_order_paginated"),
    
    path('roles/', CustomUserRoleAPIView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', CustomUserRoleAPIView.as_view(), name='role-detail'),
    
    path('download-products/', download_products_excel, name='download-products'),
    path('upload-products/', upload_products_excel, name='upload-products'),
    
    path('register-token/', register_token),
    path('send-notification/', send_notification),
    
    path('delete-expired-users/', delete_expired_users, name='delete_expired_users'),
    
    path('', include(router.urls)),

]

from django.urls import path
from . import views

urlpatterns = [
    path('get_user_cart/', views.get_user_cart, name='get_user_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item')
]

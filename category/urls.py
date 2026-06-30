from django.urls import path
from .views import category_list
from . import views

urlpatterns = [
    path('', category_list, name='category_list'),
    path('contact/', views.contact, name='contact'), 
]
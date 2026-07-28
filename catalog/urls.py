from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/add/', views.add_product, name='add_product'),
]
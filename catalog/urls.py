from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Главная страница
    path('', views.HomeView.as_view(), name='home'),

    # Контакты
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    # Детальная страница товара
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Добавление товара
    path('products/add/', views.AddProductView.as_view(), name='add_product'),
]
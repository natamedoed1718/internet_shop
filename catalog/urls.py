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

    # Создание товара
    path('products/add/', views.ProductCreateView.as_view(), name='add_product'),

    # Редактирование товара
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='update_product'),

    # Удаление товара
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
]
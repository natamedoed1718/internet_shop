from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Общедоступные страницы
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Страницы только для авторизованных пользователей
    path('products/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='update_product'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
]
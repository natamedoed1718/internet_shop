from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Список всех записей
    path('', views.BlogListView.as_view(), name='blog_list'),

    # Создание новой записи
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),

    # Просмотр отдельной записи
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),

    # Редактирование записи
    path('<int:pk>/update/', views.BlogUpdateView.as_view(), name='blog_update'),

    # Удаление записи
    path('<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
]
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # id и name в списке
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category']  # id, name, price, category
    list_filter = ['category']  # фильтрация по категории
    search_fields = ['name', 'description']  # поиск по name и description
    list_editable = ['price']  # возможность редактировать цену прямо в списке
    readonly_fields = ['created_at', 'updated_at']


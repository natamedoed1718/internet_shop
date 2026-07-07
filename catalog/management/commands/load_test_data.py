from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json
import os


class Command(BaseCommand):
    help = 'Загружает тестовые данные из фикстур'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🗑️ Удаление существующих данных...'))

        # Удаляем все данные
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Данные удалены!'))

        # Путь к фикстурам
        fixture_dir = 'catalog/fixtures/'

        # Загружаем категории
        categories_path = os.path.join(fixture_dir, 'categories.json')
        if os.path.exists(categories_path):
            with open(categories_path, 'r', encoding='utf-8') as f:
                categories_data = json.load(f)

            for item in categories_data:
                fields = item['fields']
                category = Category.objects.create(
                    name=fields['name'],
                    description=fields.get('description', '')
                )
                self.stdout.write(f'Создана категория: {category.name}')

        # Загружаем продукты
        products_path = os.path.join(fixture_dir, 'products.json')
        if os.path.exists(products_path):
            with open(products_path, 'r', encoding='utf-8') as f:
                products_data = json.load(f)

            for item in products_data:
                fields = item['fields']
                try:
                    category = Category.objects.get(name=fields['category'])
                except Category.DoesNotExist:
                    category = Category.objects.first()

                product = Product.objects.create(
                    name=fields['name'],
                    description=fields.get('description', ''),
                    category=category,
                    price=fields['price'],
                )
                self.stdout.write(f' Создан продукт: {product.name}')

        self.stdout.write(self.style.SUCCESS('🎉 Данные успешно загружены!'))

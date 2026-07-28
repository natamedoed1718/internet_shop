from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category, Contact


def home(request):
    """Контроллер для отображения домашней страницы."""
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """Контроллер для отображения страницы контактов."""
    success = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            phone='',
            address=message
        )
        success = True

    contacts_data = Contact.objects.all()

    context = {
        'success': success,
        'contacts': contacts_data,
    }
    return render(request, 'catalog/contacts.html', context)


def product_detail(request, pk):
    """
    Детальная страница товара, получает pk, извлекает объект через ORM и передает его в шаблон
    """
    product = get_object_or_404(Product, pk=pk)

    # Рекомендуемые товары (из той же категории)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=product.pk)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'catalog/product_detail.html', context)


def add_product(request):
    """Страница с формой для добавления нового товара"""
    categories = Category.objects.all()

    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        # Проверяем обязательные поля
        if not all([name, description, price, category_id]):
            messages.error(request, 'Все поля обязательны для заполнения!')
            return render(request, 'catalog/add_product.html', {
                'categories': categories,
                'name': name,
                'description': description,
                'price': price,
                'category_id': category_id,
            })

        try:
            price = float(price)
            category = Category.objects.get(id=category_id)

            # Создаем товар
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                image=image,
            )

            messages.success(request, f'Товар "{product.name}" успешно добавлен!')
            return redirect('catalog:product_detail', pk=product.pk)

        except ValueError:
            messages.error(request, 'Некорректная цена!')
        except Category.DoesNotExist:
            messages.error(request, 'Выберите существующую категорию!')

        # Если была ошибка, возвращаем форму с ошибками
        return render(request, 'catalog/add_product.html', {'categories': categories})

    # GET-запрос — показываем пустую форму
    return render(request, 'catalog/add_product.html', {'categories': categories})

from django.shortcuts import render
from .models import Product, Category, Contact


def home(request):
    """Контроллер для отображения домашней страницы."""
    products = Product.objects.all()[:6]
    categories = Category.objects.all()

    # Последние 5 продуктов (для вывода в консоль)
    latest_products = Product.objects.all().order_by('-created_at')[:5]

    print("\n" + "=" * 50)
    print("Последние 5 созданных продуктов:")
    print("=" * 50)
    for product in latest_products:
        print(f"• {product.name} (${product.price}) - {product.category.name}")
    print("=" * 50 + "\n")

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


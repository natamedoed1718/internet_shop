from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View
from .models import Product, Category, Contact


class HomeView(ListView):
    """
    Контроллер для отображения домашней страницы.
    Заменяет FBV home()
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ContactsView(View):
    """
    Контроллер для отображения страницы контактов.
    Заменяет FBV contacts()
    """

    def get(self, request):
        """GET-запрос: отображаем страницу с формой."""
        success = False
        contacts_data = Contact.objects.all()

        context = {
            'success': success,
            'contacts': contacts_data,
        }
        return render(request, 'catalog/contacts.html', context)

    def post(self, request):
        """POST-запрос: сохраняем данные из формы."""
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Создаем запись в базе данных
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


class ProductDetailView(DetailView):
    """
    Детальная страница товара с рекомендациями.
    Заменяет FBV product_detail()
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Рекомендуемые товары (из той же категории)
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(pk=product.pk)[:4]

        context['related_products'] = related_products
        return context


class AddProductView(View):
    """
    Страница с формой для добавления нового товара.
    Заменяет FBV add_product()
    """

    def get(self, request):
        """GET-запрос: показываем пустую форму."""
        categories = Category.objects.all()
        return render(request, 'catalog/add_product.html', {'categories': categories})

    def post(self, request):
        """POST-запрос: обрабатываем данные формы и сохраняем товар."""
        categories = Category.objects.all()

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
        return render(request, 'catalog/add_product.html', {
            'categories': categories,
            'name': name,
            'description': description,
            'price': price,
            'category_id': category_id,
        })

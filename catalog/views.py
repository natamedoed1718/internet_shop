from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from .models import Product, Category, Contact
from .forms import ProductForm


class HomeView(ListView):
    """Контроллер для отображения домашней страницы."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ContactsView(View):
    """Контроллер для отображения страницы контактов."""

    def get(self, request):
        success = False
        contacts_data = Contact.objects.all()

        context = {
            'success': success,
            'contacts': contacts_data,
        }
        return render(request, 'catalog/contacts.html', context)

    def post(self, request):
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


class ProductDetailView(DetailView):
    """Детальная страница товара с рекомендациями."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        related_products = Product.objects.filter(
            category=product.category
        ).exclude(pk=product.pk)[:4]

        context['related_products'] = related_products
        return context


class ProductCreateView(CreateView):
    """
    Создание нового товара с использованием формы.
    Заменяет FBV add_product()
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Добавляем сообщение об успехе."""
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{self.object.name}" успешно добавлен!')
        return response

    def form_invalid(self, form):
        """Добавляем сообщения об ошибках."""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    """
    Редактирование товара с использованием формы.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/update_product.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{self.object.name}" успешно обновлен!')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)


class ProductDeleteView(DeleteView):
    """
    Удаление товара.
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f'Товар "{product.name}" успешно удален!')
        return super().delete(request, *args, **kwargs)


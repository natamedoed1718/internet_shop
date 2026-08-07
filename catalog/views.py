from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Product, Category, Contact
from .forms import ProductForm
from django.views import View


class HomeView(ListView):
    """Главная страница - доступна всем."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """Детальная страница товара - доступна всем."""
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


class ContactsView(View):
    """Страница контактов - доступна всем."""

    def get(self, request):
        success = False
        contacts_data = Contact.objects.all()
        return render(request, 'catalog/contacts.html', {
            'success': success,
            'contacts': contacts_data,
        })

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

        return render(request, 'catalog/contacts.html', {
            'success': True,
            'contacts': Contact.objects.all(),
        })



# CRUD для продуктов - ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    """Создание товара - только для авторизованных."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{self.object.name}" успешно добавлен!')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    """Редактирование товара - только для авторизованных."""
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


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    """Удаление товара - только для авторизованных."""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f'Товар "{product.name}" успешно удален!')
        return super().delete(request, *args, **kwargs)


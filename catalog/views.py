from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def home(request):
    """
    Контроллер для отображения домашней страницы.
    """
    return render(request, 'catalog/home.html')


def contacts(request):
    """
    Контроллер для отображения страницы контактов.
    * Дополнительное задание: обработка формы обратной связи.
    """
    success = False

    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Выводим данные в консоль (для отладки)
        print(f"\nНовое сообщение от {name} ({email}):")
        print(f"{message}\n")

        # Устанавливаем флаг успешной отправки
        success = True

        # Можно добавить сохранение в базу данных позже

        # return HttpResponseRedirect(reverse('catalog:contacts') + '?success=1')

    # Передаем success в шаблон
    context = {
        'success': success,
    }

    return render(request, 'catalog/contacts.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import User


def register(request):
    """
    Регистрация нового пользователя.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Отправка приветственного письма
            try:
                send_mail(
                    subject='Добро пожаловать в наш интернет-магазин!',
                    message=f'Здравствуйте, {user.email}!\n\n'
                            f'Вы успешно зарегистрировались в нашем интернет-магазине.\n'
                            f'Теперь вы можете просматривать товары и управлять ими.\n\n'
                            f'С уважением,\n'
                            f'Команда интернет-магазина',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
                messages.success(request, 'Регистрация успешна! На вашу почту отправлено приветственное письмо.')
            except Exception as e:
                messages.warning(request, f'Регистрация успешна, но не удалось отправить письмо: {e}')

            # Автоматически авторизуем пользователя после регистрации
            login(request, user)
            return redirect('catalog:home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """
    Авторизация пользователя по email и паролю.
    """
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Аутентификация по email
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.email}!')

                # Перенаправление на страницу, с которой пришел пользователь
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('catalog:home')
            else:
                messages.error(request, 'Неверный email или пароль.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    """
    Выход пользователя.
    """
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('catalog:home')


@login_required
def profile(request):
    """
    * Дополнительное задание: Редактирование профиля пользователя.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


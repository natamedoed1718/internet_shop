from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя с расширенными полями.
    Электронная почта используется как поле для авторизации.
    """
    username = None  # Убираем поле username

    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Номер телефона'
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Страна'
    )

    USERNAME_FIELD = 'email'  # Поле для авторизации
    REQUIRED_FIELDS = []  # Обязательные поля (кроме email и password)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


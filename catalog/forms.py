from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category

# Список запрещенных слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта с валидацией."""

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название товара'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите описание товара'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Добавляем стили для всех полей (Задание 3)
        for field_name, field in self.fields.items():
            if field.widget.__class__ not in [forms.FileInput, forms.Select]:
                field.widget.attrs['class'] = 'form-control'
            elif field.widget.__class__ == forms.Select:
                field.widget.attrs['class'] = 'form-select'
            elif field.widget.__class__ == forms.FileInput:
                field.widget.attrs['class'] = 'form-control'

        # Добавляем плейсхолдеры
        self.fields['name'].widget.attrs['placeholder'] = 'Введите название товара'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание товара'
        self.fields['price'].widget.attrs['placeholder'] = '0.00'

        # Обновляем queryset для категорий
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = 'Выберите категорию'

    def clean_name(self):
        """Валидация названия на наличие запрещенных слов."""
        name = self.cleaned_data.get('name')

        if name:
            name_lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in name_lower:
                    raise ValidationError(
                        f'Название содержит запрещенное слово: "{word}". '
                        f'Пожалуйста, используйте другие формулировки.'
                    )
        return name

    def clean_description(self):
        """Валидация описания на наличие запрещенных слов."""
        description = self.cleaned_data.get('description')

        if description:
            description_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in description_lower:
                    raise ValidationError(
                        f'Описание содержит запрещенное слово: "{word}". '
                        f'Пожалуйста, используйте другие формулировки.'
                    )
        return description

    def clean_price(self):
        """
        Задание 2: Валидация цены (не может быть отрицательной).
        """
        price = self.cleaned_data.get('price')

        if price is not None:
            if price < 0:
                raise ValidationError(
                    'Цена не может быть отрицательной. '
                    'Пожалуйста, введите корректную цену.'
                )
            elif price == 0:
                raise ValidationError(
                    'Цена не может быть равна нулю. '
                    'Пожалуйста, введите корректную цену.'
                )
        return price

    def clean_image(self):
        """
        * Дополнительное задание: Валидация изображения.
        Проверяем формат (JPEG, PNG) и размер (не более 5 МБ).
        """
        image = self.cleaned_data.get('image')

        if image:
            # Проверяем размер файла (максимум 5 МБ = 5 * 1024 * 1024 байт)
            max_size = 5 * 1024 * 1024  # 5 МБ
            if image.size > max_size:
                raise ValidationError(
                    f'Размер файла превышает 5 МБ. '
                    f'Текущий размер: {image.size / 1024 / 1024:.2f} МБ. '
                    f'Пожалуйста, сожмите изображение.'
                )

            # Проверяем формат файла
            valid_extensions = ['jpg', 'jpeg', 'png']
            file_extension = image.name.split('.')[-1].lower()

            if file_extension not in valid_extensions:
                raise ValidationError(
                    f'Неподдерживаемый формат файла. '
                    f'Разрешены только: {", ".join(valid_extensions)}. '
                    f'Текущий формат: {file_extension}'
                )

            # Проверяем MIME-тип (дополнительная проверка)
            content_type = image.content_type
            if content_type not in ['image/jpeg', 'image/png']:
                raise ValidationError(
                    f'Неподдерживаемый тип файла. '
                    f'Разрешены только: JPEG, PNG.'
                )

        return image



# catalog/forms.py
from decimal import Decimal, InvalidOperation
from django import forms
from django.core.exceptions import ValidationError
from .models import Product
from .constants import BANNED_WORDS

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "image": forms.ClearableFileInput(),
            "category": forms.Select(),
            "price": forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({"class": "form-check-input"})
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs.update({"class": "form-control-file"})
            elif isinstance(widget, forms.Select):
                widget.attrs.update({"class": "form-select"})
            else:
                widget.attrs.update({"class": "form-control", "placeholder": field.label or ""})

    def _check_banned(self, value, field_verbose):
        """Проверяет наличие запрещённого слова (case-insensitive)."""
        if not value:
            return
        text = str(value).lower()
        for bad in BANNED_WORDS:
            if bad in text:
                raise ValidationError(f'В поле «{field_verbose}» запрещено использовать слово «{bad}».')

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        self._check_banned(name, "Наименование")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        self._check_banned(description, "Описание")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None:
            return price
        try:
            price_dec = Decimal(price)
        except (InvalidOperation, TypeError):
            raise ValidationError("Цена должна быть числом.")
        if price_dec < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price_dec

"""
Формы интерфейса: фильтры и форма записи ДДС.
"""

from __future__ import annotations

from django import forms
from django.utils import timezone

from cashflow.models import Cashflow
from directories.models import Category, Status, Subcategory, Type


class CashflowFilterForm(forms.Form):
    """Форма фильтров для списка записей ДДС."""

    date_from = forms.DateTimeField(
        label="С даты",
        required=False,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
    )
    date_to = forms.DateTimeField(
        label="По дату",
        required=False,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
    )
    status = forms.ModelChoiceField(
        label="Статус",
        queryset=Status.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    type = forms.ModelChoiceField(
        label="Тип",
        queryset=Type.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "hx-get": "",
                "hx-target": "#id_category",
                "hx-trigger": "change",
            }
        ),
    )
    category = forms.ModelChoiceField(
        label="Категория",
        queryset=Category.objects.none(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "hx-get": "",
                "hx-target": "#id_subcategory",
                "hx-trigger": "change",
            }
        ),
    )
    subcategory = forms.ModelChoiceField(
        label="Подкатегория",
        queryset=Subcategory.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs) -> None:
        """Инициализация с учётом выбранных значений для каскадов."""
        super().__init__(*args, **kwargs)

        # Подставим реальные эндпоинты для HTMX (заполним hx-get динамически)
        self.fields["type"].widget.attrs["hx-get"] = "/htmx/types/categories/"
        self.fields["category"].widget.attrs[
            "hx-get"
        ] = "/htmx/categories/subcategories/"

        data = self.data if self.is_bound else {}
        type_id = data.get("type") or None
        category_id = data.get("category") or None

        if type_id:
            self.fields["category"].queryset = Category.objects.filter(
                type_id=type_id
            ).order_by("name")
        else:
            self.fields["category"].queryset = Category.objects.none()

        if category_id:
            self.fields["subcategory"].queryset = Subcategory.objects.filter(
                category_id=category_id
            ).order_by("name")
        else:
            self.fields["subcategory"].queryset = Subcategory.objects.none()


class CashflowForm(forms.ModelForm):
    """Форма создания/редактирования записи ДДС с каскадными селектами."""

    created_at = forms.DateTimeField(
        label="Дата/время",
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    # В форме держим «виртуальные» поля type и category для UX, но сохраняем
    # только subcategory/status.
    type = forms.ModelChoiceField(
        label="Тип",
        queryset=Type.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "hx-get": "/htmx/types/categories/",
                "hx-target": "#id_category",
                "hx-trigger": "change",
                "required": "required",
            }
        ),
    )
    category = forms.ModelChoiceField(
        label="Категория",
        queryset=Category.objects.none(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "hx-get": "/htmx/categories/subcategories/",
                "hx-target": "#id_subcategory",
                "hx-trigger": "change",
                "required": "required",
            }
        ),
    )

    class Meta:
        model = Cashflow
        fields = [
            "created_at",
            "status",
            "type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]
        widgets = {
            "created_at": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "subcategory": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(
                attrs={"step": "0.01", "class": "form-control"}
            ),
            "comment": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
        }
        labels = {
            "created_at": "Дата/время",
            "status": "Статус",
            "subcategory": "Подкатегория",
            "amount": "Сумма",
            "comment": "Комментарий",
        }

    def __init__(self, *args, **kwargs) -> None:
        """Инициализация каскадов type - category - subcategory."""
        super().__init__(*args, **kwargs)

        # created_at: чтобы на create подставлялось "сейчас",
        # а на edit — текущее значение
        if self.instance and self.instance.pk:
            if self.instance.created_at:
                self.initial["created_at"] = self.instance.created_at.strftime(
                    "%Y-%m-%dT%H:%M"
                )
        else:
            if not self.is_bound:
                self.initial["created_at"] = timezone.now().strftime(
                    "%Y-%m-%dT%H:%M"
                )

        # Когда редактируем существующую запись — заполняем каскад из instance
        if self.instance and self.instance.pk:
            subcat = self.instance.subcategory
            cat = subcat.category
            typ = cat.type
            self.fields["type"].initial = typ.pk
            self.fields["category"].queryset = Category.objects.filter(
                type=typ
            ).order_by("name")
            self.fields["category"].initial = cat.pk
            self.fields["subcategory"].queryset = Subcategory.objects.filter(
                category=cat
            ).order_by("name")
            return

        # Когда форма привязана к данным (POST/GET) — подставим queryset'ы
        # по выбранным значениям
        data = self.data if self.is_bound else {}
        type_id = data.get("type") or None
        category_id = data.get("category") or None

        if type_id:
            self.fields["category"].queryset = Category.objects.filter(
                type_id=type_id
            ).order_by("name")
        else:
            self.fields["category"].queryset = Category.objects.none()

        if category_id:
            self.fields["subcategory"].queryset = Subcategory.objects.filter(
                category_id=category_id
            ).order_by("name")
        else:
            self.fields["subcategory"].queryset = Subcategory.objects.none()

    def clean(self) -> dict:
        """
        Валидация каскадов (не сохраняем type/category,
        но сверяем согласованность).
        """
        cleaned = super().clean()
        type_obj = cleaned.get("type")
        category_obj = cleaned.get("category")
        subcat_obj = cleaned.get("subcategory")

        if category_obj and type_obj and category_obj.type_id != type_obj.id:
            self.add_error(
                "category", "Категория не принадлежит выбранному типу."
            )

        if (
            subcat_obj
            and category_obj
            and subcat_obj.category_id != category_obj.id
        ):
            self.add_error(
                "subcategory",
                "Подкатегория не принадлежит выбранной категории.",
            )

        return cleaned

    def clean_created_at(self):
        """
        Если поле не трогали:
        - на create — подставим now()
        - на edit — оставим старое значение instance.created_at
        """
        value = self.cleaned_data.get("created_at")
        if value:
            return value
        # пусто
        if self.instance and self.instance.pk and self.instance.created_at:
            return self.instance.created_at
        from django.utils import timezone

        return timezone.now()

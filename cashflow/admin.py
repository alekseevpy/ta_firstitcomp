"""
Админка для записей ДДС.

Отображает вычисляемые поля: тип и категория через связи подкатегории.
"""

from __future__ import annotations

from django.contrib import admin

from .models import Cashflow


@admin.register(Cashflow)
class CashflowAdmin(admin.ModelAdmin):
    """Настройки отображения записей ДДС."""

    list_display = (
        "created_at",
        "amount",
        "status",
        "type_name",
        "category_name",
        "subcategory_name",
        "short_comment",
    )
    list_filter = (
        "status",
        "subcategory__category__type",
        "subcategory__category",
    )
    search_fields = ("comment",)
    date_hierarchy = "created_at"
    ordering = ("-created_at", "-id")

    def type_name(self, obj: Cashflow) -> str:
        """Возвращает название типа для строки списка.

        Args:
            obj (Cashflow): текущая запись.

        Returns:
            str: название типа.
        """
        return obj.type.name

    type_name.short_description = "Тип"
    type_name.admin_order_field = "subcategory__category__type__name"

    def category_name(self, obj: Cashflow) -> str:
        """Возвращает название категории для строки списка.

        Args:
            obj (Cashflow): текущая запись.

        Returns:
            str: название категории.
        """
        return obj.category.name

    category_name.short_description = "Категория"
    category_name.admin_order_field = "subcategory__category__name"

    def subcategory_name(self, obj: Cashflow) -> str:
        """Возвращает название подкатегории для строки списка.

        Args:
            obj (Cashflow): текущая запись.

        Returns:
            str: название подкатегории.
        """
        return obj.subcategory.name

    subcategory_name.short_description = "Подкатегория"
    subcategory_name.admin_order_field = "subcategory__name"

    def short_comment(self, obj: Cashflow) -> str:
        """Короткий комментарий для списка.

        Args:
            obj (Cashflow): текущая запись.

        Returns:
            str: обрезанный комментарий.
        """
        return (obj.comment or "")[:40] + (
            "…" if obj.comment and len(obj.comment) > 40 else ""
        )

    short_comment.short_description = "Комментарий"

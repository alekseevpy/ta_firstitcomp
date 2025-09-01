"""
Админка для справочников.

Управление Типами, Категориями, Подкатегориями и Статусами.
"""

from __future__ import annotations

from django.contrib import admin

from .models import Category, Status, Subcategory, Type


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    """Настройки отображения типов операций."""

    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройки отображения категорий операций."""

    list_display = ("name", "type")
    search_fields = ("name",)
    list_filter = ("type",)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Настройки отображения подкатегорий операций."""

    list_display = ("name", "category")
    search_fields = ("name",)
    list_filter = ("category",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Настройки отображения статусов операций."""

    list_display = ("name", "code", "is_active")
    search_fields = ("name", "code")
    list_filter = ("is_active",)

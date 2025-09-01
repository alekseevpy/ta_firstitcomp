"""
Справочники: Type, Category, Subcategory, Status.

Содержит иерархию: Type - Category - Subcategory и Status
"""

from __future__ import annotations

from django.db import models


class Type(models.Model):
    """Тип операции."""

    name: models.CharField = models.CharField(
        "Название типа", max_length=100, unique=True
    )
    is_active: models.BooleanField = models.BooleanField(
        "Активен", default=True
    )

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """Категория операции, связанная с конкретным типом."""

    type: models.ForeignKey = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Тип",
    )
    name: models.CharField = models.CharField(
        "Название категории", max_length=100
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ("type", "name")
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.type.name})"


class Subcategory(models.Model):
    """Подкатегория, связанная с конкретной категорией."""

    category: models.ForeignKey = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория",
    )
    name: models.CharField = models.CharField(
        "Название подкатегории", max_length=100
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        unique_together = ("category", "name")
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.category.name})"


class Status(models.Model):
    """Статус операции."""

    name: models.CharField = models.CharField(
        "Название статуса", max_length=50, unique=True
    )
    code: models.CharField = models.CharField(
        "Код статуса", max_length=50, unique=True
    )
    is_active: models.BooleanField = models.BooleanField(
        "Активен", default=True
    )

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

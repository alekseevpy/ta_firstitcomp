"""
DRF сериализаторы для справочников.
"""

from __future__ import annotations

from rest_framework import serializers

from .models import Category, Status, Subcategory, Type


class TypeSerializer(serializers.ModelSerializer):
    """Сериализатор типа операции."""

    class Meta:
        model = Type
        fields = ["id", "name", "is_active"]


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории операции."""

    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all())

    class Meta:
        model = Category
        fields = ["id", "name", "type"]


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории операции."""

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Subcategory
        fields = ["id", "name", "category"]


class StatusSerializer(serializers.ModelSerializer):
    """Сериализатор статуса операции."""

    class Meta:
        model = Status
        fields = ["id", "name", "code", "is_active"]

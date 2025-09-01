"""
DRF сериализаторы для записей ДДС.
"""

from __future__ import annotations

from rest_framework import serializers

from directories.models import Status, Subcategory

from .models import Cashflow


class CashflowSerializer(serializers.ModelSerializer):
    """CRUD сериализатор для Cashflow.

    На запись принимаем: created_at, status, subcategory, amount, comment.
    На чтение дополнительно отдаём вычисляемые: category, type.
    """

    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=Subcategory.objects.select_related(
            "category", "category__type"
        ).all()
    )

    # read-only поля, вычисляются через связи
    category = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cashflow
        fields = [
            "id",
            "created_at",
            "status",
            "subcategory",
            "amount",
            "comment",
            "category",
            "type",
        ]
        read_only_fields = ["id", "category", "type"]

    def get_category(self, obj: Cashflow) -> dict | None:
        """Возвращает категорию как словарь."""
        cat = obj.category
        return {"id": cat.id, "name": cat.name} if cat else None

    def get_type(self, obj: Cashflow) -> dict | None:
        """Возвращает тип как словарь."""
        t = obj.type
        return {"id": t.id, "name": t.name} if t else None

"""
Фильтры для API.
"""

from __future__ import annotations

import django_filters
from django.db.models import QuerySet

from cashflow.models import Cashflow


class CashflowFilter(django_filters.FilterSet):
    """Фильтры записей ДДС: период дат и справочники."""

    date_from = django_filters.IsoDateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    date_to = django_filters.IsoDateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    status = django_filters.NumberFilter(field_name="status_id")

    # фильтры по иерархии через связи
    type = django_filters.NumberFilter(
        field_name="subcategory__category__type_id"
    )
    category = django_filters.NumberFilter(
        field_name="subcategory__category_id"
    )
    subcategory = django_filters.NumberFilter(field_name="subcategory_id")

    ordering = django_filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("amount", "amount"),
            ("id", "id"),
        ),
        field_labels={"created_at": "Дата", "amount": "Сумма", "id": "ID"},
    )

    class Meta:
        model = Cashflow
        fields = [
            "date_from",
            "date_to",
            "status",
            "type",
            "category",
            "subcategory",
        ]

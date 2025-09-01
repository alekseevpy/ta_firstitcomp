"""
API-вьюхи DRF для записей ДДС (CRUD + фильтры).
"""

from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.filters import CashflowFilter

from .models import Cashflow
from .serializers import CashflowSerializer


class CashflowViewSet(viewsets.ModelViewSet):
    """CRUD эндпоинты для записей ДДС."""

    queryset = (
        Cashflow.objects.select_related(
            "status",
            "subcategory",
            "subcategory__category",
            "subcategory__category__type",
        )
        .all()
        .order_by("-created_at", "-id")
    )
    serializer_class = CashflowSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CashflowFilter

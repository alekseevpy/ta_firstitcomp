"""
API-вьюхи DRF для справочников и каскадных списков.
"""

from __future__ import annotations

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Status, Subcategory, Type
from .serializers import (
    CategorySerializer,
    StatusSerializer,
    SubcategorySerializer,
    TypeSerializer,
)


class TypeViewSet(viewsets.ModelViewSet):
    """CRUD для типов операции."""

    queryset = Type.objects.all().order_by("name")
    serializer_class = TypeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD для категорий."""

    queryset = Category.objects.select_related("type").all().order_by("name")
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):
    """CRUD для подкатегорий."""

    queryset = (
        Subcategory.objects.select_related("category", "category__type")
        .all()
        .order_by("name")
    )
    serializer_class = SubcategorySerializer


class StatusViewSet(viewsets.ModelViewSet):
    """CRUD для статусов."""

    queryset = Status.objects.all().order_by("name")
    serializer_class = StatusSerializer


class TypeCascadeViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Каскады для типов: получить список категорий по type_id."""

    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    @action(detail=True, methods=["get"], url_path="categories")
    def categories(self, request, pk: str) -> Response:
        """Возвращает категории для заданного типа."""
        qs = Category.objects.filter(type_id=pk).order_by("name")
        data = CategorySerializer(qs, many=True).data
        return Response(data)


class CategoryCascadeViewSet(
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Каскады для категорий: получить список подкатегорий по category_id."""

    queryset = Category.objects.select_related("type").all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=["get"], url_path="subcategories")
    def subcategories(self, request, pk: str) -> Response:
        """Возвращает подкатегории для заданной категории."""
        qs = Subcategory.objects.filter(category_id=pk).order_by("name")
        data = SubcategorySerializer(qs, many=True).data
        return Response(data)

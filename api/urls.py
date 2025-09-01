"""
URL DRF API: справочники, каскадные эндпоинты, ДДС.
"""

from __future__ import annotations

from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.routers import router
from cashflow.views import CashflowViewSet
from directories.views import (
    CategoryCascadeViewSet,
    CategoryViewSet,
    StatusViewSet,
    SubcategoryViewSet,
    TypeCascadeViewSet,
    TypeViewSet,
)

# Регистрируем CRUD роуты
router.register(r"types", TypeViewSet, basename="types")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"subcategories", SubcategoryViewSet, basename="subcategories")
router.register(r"statuses", StatusViewSet, basename="statuses")
router.register(r"cashflows", CashflowViewSet, basename="cashflows")

# Каскадные роуты
router.register(r"types-cascade", TypeCascadeViewSet, basename="types-cascade")
router.register(
    r"categories-cascade",
    CategoryCascadeViewSet,
    basename="categories-cascade",
)


@api_view(["GET"])
def health(_request):
    """Проверка API."""
    return Response({"status": "ok"})


urlpatterns = [
    path("health/", health, name="api-health"),
    path("", include(router.urls)),
]

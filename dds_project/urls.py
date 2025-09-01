"""
Глобальный маршрутизатор проекта.
"""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

# Документация
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API (CRUD, каскады, health и т.п. объявлены в api.urls)
    path("api/", include("api.urls")),
    # UI
    path("", include("ui.urls")),
    # JSON-схема OpenAPI 3.0
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # ReDoc UI
    path(
        "api/docs/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Swagger UI
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

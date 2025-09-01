"""
Маршруты UI: список, CRUD, HTMX-каскады.
"""

from __future__ import annotations

from django.urls import path

from .views import (
    cashflow_create,
    cashflow_delete,
    cashflow_list,
    cashflow_update,
    htmx_categories_options,
    htmx_subcategories_options,
)

urlpatterns = [
    path("", cashflow_list, name="cashflow-list"),
    path("create/", cashflow_create, name="cashflow-create"),
    path("<int:pk>/edit/", cashflow_update, name="cashflow-update"),
    path("<int:pk>/delete/", cashflow_delete, name="cashflow-delete"),
    # HTMX endpoints: возвращают набор <option>… по выбранному значению
    path(
        "htmx/types/categories/",
        htmx_categories_options,
        name="htmx-type-categories",
    ),
    path(
        "htmx/categories/subcategories/",
        htmx_subcategories_options,
        name="htmx-category-subcategories",
    ),
]

"""
Вьюхи UI: список с фильтрами и CRUD формой, HTMX-каскады.
"""

from __future__ import annotations

from decimal import Decimal

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import QuerySet, Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from cashflow.models import Cashflow
from directories.models import Category, Subcategory

from .forms import CashflowFilterForm, CashflowForm


@require_GET
def cashflow_list(request: HttpRequest) -> HttpResponse:
    """Список записей ДДС с фильтрами и пагинацией."""
    form = CashflowFilterForm(request.GET or None)

    qs: QuerySet[Cashflow] = (
        Cashflow.objects.select_related(
            "status",
            "subcategory",
            "subcategory__category",
            "subcategory__category__type",
        )
        .all()
        .order_by("-created_at", "-id")
    )

    if form.is_valid():
        cd = form.cleaned_data
        if cd.get("date_from"):
            qs = qs.filter(created_at__gte=cd["date_from"])
        if cd.get("date_to"):
            qs = qs.filter(created_at__lte=cd["date_to"])
        if cd.get("status"):
            qs = qs.filter(status=cd["status"])
        if cd.get("subcategory"):
            qs = qs.filter(subcategory=cd["subcategory"])
        elif cd.get("category"):
            qs = qs.filter(subcategory__category=cd["category"])
        elif cd.get("type"):
            qs = qs.filter(subcategory__category__type=cd["type"])

    # Пагинация
    paginator = Paginator(qs, 20)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)

    # Итог по видимым строкам (страница) и по всему выбору
    page_total = sum(
        (obj.amount for obj in page_obj.object_list), start=Decimal("0.00")
    )
    full_total = qs.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    ctx = {
        "form": form,
        "page_obj": page_obj,
        "page_total": page_total,
        "full_total": full_total,
    }
    return render(request, "cashflow_list.html", ctx)


@require_http_methods(["GET", "POST"])
def cashflow_create(request: HttpRequest) -> HttpResponse:
    """Создание записи ДДС."""
    form = CashflowForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Запись успешно создана.")
        return redirect("cashflow-list")
    return render(request, "cashflow_form.html", {"form": form})


@require_http_methods(["GET", "POST"])
def cashflow_update(request: HttpRequest, pk: int) -> HttpResponse:
    """Редактирование записи ДДС."""
    obj = get_object_or_404(Cashflow, pk=pk)
    form = CashflowForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Изменения сохранены.")
        return redirect("cashflow-list")
    return render(request, "cashflow_form.html", {"form": form, "object": obj})


@require_http_methods(["POST"])
def cashflow_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаление записи ДДС."""
    obj = get_object_or_404(Cashflow, pk=pk)
    obj.delete()
    messages.info(request, "Запись удалена.")
    return redirect("cashflow-list")


@require_GET
def htmx_categories_options(request: HttpRequest) -> HttpResponse:
    """Отдаёт <option> для категорий по type_id (для фильтра/формы)."""
    type_id = request.GET.get("type")
    categories = (
        Category.objects.filter(type_id=type_id).order_by("name")
        if type_id
        else Category.objects.none()
    )
    return render(request, "includes/_options.html", {"objects": categories})


@require_GET
def htmx_subcategories_options(request: HttpRequest) -> HttpResponse:
    """Отдаёт <option> для подкатегорий по category_id (для фильтра/формы)."""
    category_id = request.GET.get("category")
    subcategories = (
        Subcategory.objects.filter(category_id=category_id).order_by("name")
        if category_id
        else Subcategory.objects.none()
    )
    return render(
        request, "includes/_options.html", {"objects": subcategories}
    )

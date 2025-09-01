"""
Модель движения денежных средств.

Хранит факт операции с суммой, датой, статусом и подкатегорией.
Категория и тип получаются через связи от подкатегории:
Subcategory - Category - Type.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Optional

from django.db import models
from django.utils import timezone

from directories.models import Category, Status, Subcategory, Type


class Cashflow(models.Model):
    """Запись ДДС: сумма, дата, статус и подкатегория."""

    created_at: models.DateTimeField = models.DateTimeField(
        "Дата/время операции",
        default=timezone.now,
        db_index=True,
    )
    status: models.ForeignKey = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="cashflows",
        verbose_name="Статус",
        db_index=True,
    )
    subcategory: models.ForeignKey = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        related_name="cashflows",
        verbose_name="Подкатегория",
        db_index=True,
    )
    amount: models.DecimalField = models.DecimalField(
        "Сумма",
        max_digits=12,
        decimal_places=2,
    )
    comment: models.TextField = models.TextField("Комментарий", blank=True)

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["subcategory"]),
        ]

    def __str__(self) -> str:
        """Возвращает человекочитаемое представление записи.

        Args:
            None

        Returns:
            str: строка с датой, суммой и статусом.
        """
        return (
            f"{self.created_at:%Y-%m-%d %H:%M} · ",
            f"{self.amount} · {self.status.name}",
        )

    @property
    def category(self) -> Category:
        """Возвращает категорию через связь подкатегории.

        Args:
            None

        Returns:
            Category: категория, к которой принадлежит подкатегория.
        """
        return self.subcategory.category

    @property
    def type(self) -> Type:
        """Возвращает тип через цепочку подкатегория → категория → тип.

        Args:
            None

        Returns:
            Type: тип операции (например, Пополнение/Списание).
        """
        return self.subcategory.category.type

    def clean(self) -> None:
        """Проводит базовую проверку целостности данных.

        Args:
            None

        Returns:
            None: выбросит ValidationError при несоответствиях.
        """
        return None

    def is_income(self) -> bool:
        """Проверяет, является ли операция «пополнением».

        Args:
            None

        Returns:
            bool: True, если тип операции — Пополнение.
        """
        return self.type.name.lower() == "пополнение"

    def is_outcome(self) -> bool:
        """Проверяет, является ли операция «списанием».

        Args:
            None

        Returns:
            bool: True, если тип операции — Списание.
        """
        return self.type.name.lower() == "списание"

    def abs_amount(self) -> Decimal:
        """Возвращает модуль суммы.

        Args:
            None

        Returns:
            Decimal: абсолютное значение суммы.
        """
        return abs(self.amount)

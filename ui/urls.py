"""
Заглушка.
"""

from django.urls import path

from .views import cashflow_list

urlpatterns = [path("", cashflow_list, name="cashflow-list")]

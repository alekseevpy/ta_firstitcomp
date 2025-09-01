"""
Заглушка.
"""

from django.http import JsonResponse
from django.urls import path


def api_health(_):
    return JsonResponse({"status": "ok"})


urlpatterns = [path("health/", api_health, name="api-health")]

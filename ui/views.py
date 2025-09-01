"""
Заглушка.
"""

from django.shortcuts import render


def cashflow_list(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    return render(request, "ui/cashflow_list.html", {})

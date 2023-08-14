from django.shortcuts import render  # noqa F401
from django.views.generic.detail import DetailView
from .models import Shop


class ShopDetailView(DetailView):
    """View детального представления магазина"""

    template_name = "shop/shop_detail.jinja2"
    model = Shop

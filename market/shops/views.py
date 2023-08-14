from django.shortcuts import render  # noqa F401
from django.views.generic.detail import DetailView
from .models import Shop, Offer
from products.models import Product
from django.http import HttpRequest, HttpResponse


class ShopDetailView(DetailView):
    """View детального представления магазина"""

    template_name = "shop/shop_detail.jinja2"
    model = Shop

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        shop = Shop.objects.get(pk=pk)
        offer = Offer.objects.filter(shop_id=shop.pk)
        product = Product.objects.get(pk=pk)

        context = {
            "product": product,
            "shop": shop,
            "offer": offer
        }
        return render(request, "shop/shop_detail.jinja2", context=context)

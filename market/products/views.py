from django.shortcuts import render  # noqa F401
from django.views import View
from django.http import HttpRequest, HttpResponse
from shops.models import (
    Offer,
)
from .models import (
    Product,
    ProductDetail,
)


class ProductDetailViev(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        offer = Offer.objects.filter(product_id=pk)
        product = Product.objects.get(pk=pk)
        product_detail = ProductDetail.objects.get(product_id=pk)
        context = {
            "offers": offer,
            "product": product,
            "product_detail": product_detail,
            "min_price": min([off.price for off in offer]),
        }
        return render(request, "products/product-detail.jinja2", context=context)

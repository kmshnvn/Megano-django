from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.db.models import Min
from shops.models import (
    Offer,
)
from .models import (
    ProductDetail,
)


class ProductDetailViev(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        offers = Offer.objects.prefetch_related("shop").filter(product_id=pk)
        product_details = ProductDetail.objects.prefetch_related("detail", "product").get(product_id=pk)
        context = {
            "offers": offers,
            "product": product_details.product,
            "product_detail": product_details,
            "min_price": offers.aggregate(Min("price"))["price__min"],
        }
        return render(request, "products/product-detail.jinja2", context=context)

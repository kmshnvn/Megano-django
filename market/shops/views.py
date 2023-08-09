from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from .models import (
    Offer,
    Shop,
)
from products.models import (
    Product,
ProductDetail,
)


class ProductDetailViev(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        offer = Offer.objects.filter(product_id=pk)
        product  = Product.objects.get(pk=pk)
        product_detail = ProductDetail.objects.get(product_id=pk)
        context = {
            "offers": offer,
            "product": product,
            "product_detail": product_detail,
        }
        return render(request, 'shops/product-detail.jinja2', context=context)

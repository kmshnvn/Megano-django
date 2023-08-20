from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from .models import Basket
from .basket import BasketObject
from shops.models import Offer
from django.views.generic import TemplateView, ListView
from .forms import BasketAddProductForm



class BasketView(ListView):
    model = Basket
    template_name = "basket/basket-view.jinja2"
    context_object_name = "basket"

def add_product(request: HttpRequest, product_pk: int, offer_pk: int=None):
    form = BasketAddProductForm(request.POST)
    if request.method == "POST" and form.is_valid():
            cd = form.cleaned_data
            basket = BasketObject(request=request)
            basket.add_product_in_basket(
                request=request,
                product_pk=product_pk,
                offer_pk= offer_pk,
                amount=cd["amount"],
            )
    return   redirect(to='products:product_detail', pk=product_pk)


    # def get(self, request: HttpRequest) -> HttpResponse:
    #         basket = BasketObject(request)
    #
    #         return render(request, "basket/basket-view.jinja2", context={"basket":basket})
    #
    # def post(self, request: HttpRequest) -> HttpResponse:
    #     postdata = request.POST.copy()
    #     if postdata["submit"] == "add":
    #         print()
    #     return render(request, "basket/basket-view.jinja2")

    # if request.method == "POST" and 'edit' in request.POST:
    #     / Do /
    # if request.method == "POST" and 'delete' in request.POST:
    #     / Do /
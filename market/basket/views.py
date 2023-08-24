from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from .models import Basket
from .basket import BasketObject
from shops.models import Offer
from django.views.generic import TemplateView, ListView
from .forms import BasketAddProductForm


class BasketView(View):
    """
    Представление для отображения корзины
    """
    def get(self, request: HttpRequest):
        basket = BasketObject(request=request)
        return render(request, "basket/basket-view.jinja2", {"basket": basket})


def add_product(request: HttpRequest, product_pk: int, offer_pk=None):
    """Представление для добавления продукта в корзину"""
    if request.method == "POST":
        form = BasketAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            amount = cd["amount"]
    else:
        amount = 1
    basket = BasketObject(request=request)
    basket.add_product_in_basket(
        request=request,
        product_pk=product_pk,
        offer_pk= offer_pk,
        amount=amount,
    )
    return   redirect(to='products:product_detail', pk=product_pk)


def remove_product(request: HttpRequest, offer_pk: int):
    """Представление для удаления продукта из корзины"""
    if request.method == "GET":
        basket = BasketObject(request=request)
        basket.remove_product(offer_pk=offer_pk)
    return redirect(to="basket:basket_view")


def change_amount_for_product_in_basket(request: HttpRequest, offer_pk: int,amount: str):
    """Представление для изменения количество товара в корзине"""
    if request.method == "GET":
        amount = int(amount)
        basket = BasketObject(request=request)
        basket.update_product_in_basket(offer_pk=offer_pk, amount=amount)
    return  redirect(to="basket:basket_view")

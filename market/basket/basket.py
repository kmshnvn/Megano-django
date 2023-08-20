from decimal import Decimal
from products.models import Product
from shops.models import Offer
from django.http import HttpRequest
from .models import Basket
from django.conf import settings
import random
from copy import deepcopy


class BasketObject(object):
    """Инициализируем работу корзины для добавления товаров"""

    def __init__(self, request: HttpRequest) -> None:
        """Инициализация корзины в сессии"""
        self.session = request.session
        self.user = request.user
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.create_basket_for_user() if self.user.is_authenticated else {}
            self.session[settings.BASKET_SESSION_ID] = basket
        self.basket = basket

    def create_basket_for_user(self):
        basket = {}
        users_basket = Basket.objects.filter(user=self.user).prefetch_related("offers")
        for user_basket in users_basket:
            basket[user_basket.offers.pk] = {
                "product": user_basket.offers.product,
                "amount":   user_basket.amount,
                "price": str(user_basket.offers.price)
            }
        return basket

    def add_product_in_basket(self,request: HttpRequest, product_pk, offer_pk, amount: int) -> None:
        """Метод для добавления продукта в корзину"""
        if offer_pk is None:
            offers_ids = Offer.objects.filter(product_id=int(product_pk))
            offer_pk = random.choice([o_i.pk for o_i in offers_ids])
        if offer_pk in self.basket:
            self.update_product_in_basket(amount=amount, offer_pk=offer_pk)
        else:
            self.add_new_product_in_basket(offer_pk=offer_pk, amount=amount)

    def update_product_in_basket(self, amount: int, offer_pk):
        if Basket.objects.filter(user=self.user, offers=offer_pk).exist():
            user_basket = Basket.objects.only("amount").get(user=self.user, offers=offer_pk)
            user_basket.amount += amount
            user_basket.save()
        self.basket[offer_pk]["amount"] += amount

    def add_new_product_in_basket(self, offer_pk, amount):
        offer = Offer.objects.get(pk=offer_pk)
        self.basket[offer_pk] = {
            "product": offer.product,
            "amount": amount,
            "price": str(offer.price)
        }
        print(self.basket)
        self.save()


    def __iter__(self):
        print(self.basket)
        offers_pk = [key for key in self.basket.keys()]
        offers = Offer.objects.prefetch_related("product").filter(pk__in=offers_pk)

        basket = self.basket.deepcopy()
        for item in basket.values():
            yield item

    def remove_product(self, offer:Offer):
        """Метод для удаления продукта из корзины"""
        if offer.pk in self.basket:
            del self.basket[offer.pk]
            self.save()

    def remove_data_basket(self, request:HttpRequest):
        """Метод для удаления корзины из сессии"""
        del self.session[request.user]


    def get_total_price(self):
        """Подсчет стоимости всех продуктов в корзине"""
        return sum([price["price"]for price in self.basket.values()])

    def save(self):
        """Метод для сохранения корзины в сессии"""
        self.session[settings.BASKET_SESSION_ID] = self.basket
        self.session.modified = True

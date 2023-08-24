from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product
from shops.models import Offer
from django.contrib.auth.models import User


class Basket(models.Model):
    """Корзина"""

    class Meta:
        verbose_name = _("Корзина пользователя")

    user = models.ForeignKey(
        User,
        related_name="Пользователь",
        verbose_name=_("Пользователь корзины"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    offer = models.ForeignKey(
        Offer, related_name="Предложение", verbose_name=_("Предложения магазинов"), null=True, on_delete=models.PROTECT
    )

    product = models.ForeignKey(
        Product, related_name="Продукт", verbose_name=_("Продукт магазина"), null=True, on_delete=models.PROTECT
    )

    amount = models.PositiveIntegerField(verbose_name=_("Количество"), default=0)

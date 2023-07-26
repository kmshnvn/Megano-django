from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class Shop(models.Model):
    """Магазин"""

    name = models.CharField(max_length=512, verbose_name=_("название"))
    products = models.ManyToManyField(
        "products.Product",
        through="Offer",
        related_name="shops",
        verbose_name=_("товары в магазине"),
    )
    phoneNumberIsValid = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberIsValid], max_length=16, blank=True, unique=True)
    adress = models.CharField(max_length=512, blank=True, verbose_name=_("адресс"))
    email = models.EmailField(max_length=127, blank=True, verbose_name=_("почта"))
    legal_adress = models.CharField(max_length=512, blank=True, verbose_name=_("юридический адресс"))


class Offer(models.Model):
    """Предложение магазина"""

    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена"))

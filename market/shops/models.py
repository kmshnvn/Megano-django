from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from profiles.models import User

phoneNumberIsValid = RegexValidator(regex=r"^\+?1?\d{8,15}$")


class Shop(models.Model):
    """Магазин"""

    class Meta:
        verbose_name = _("магазин")
        verbose_name_plural = _("магазины")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, verbose_name=_("название"))
    products = models.ManyToManyField(
        "products.Product",
        through="Offer",
        related_name="shops",
        verbose_name=_("товары в магазине"),
    )
    phoneNumber = models.CharField(validators=[phoneNumberIsValid], max_length=16)
    adress = models.CharField(max_length=512, verbose_name=_("адресс"))
    email = models.EmailField(max_length=127, verbose_name=_("почта"))
    legal_adress = models.CharField(max_length=512, verbose_name=_("юридический адресс"))

    def __str__(self) -> str:
        return f"Shop(pk={self.pk}, name={self.name!r})"


class Offer(models.Model):
    """Предложение магазина"""

    class Meta:
        verbose_name = _("предложение")
        verbose_name_plural = _("предложения")

    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    product = models.ForeignKey("products.Product", related_name="offers", on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена"))
    remainder = models.IntegerField(default=0, verbose_name=_("остаток"))

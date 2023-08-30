from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.utils import IntegrityError


class Profile(models.Model):
    """Профиль пользователя"""

    regex_phone = RegexValidator(
        regex=r"^((8|\+7|)(\d{10}))$", message=_("Формат номера телефона должен быть: +79999999999 или 89999999999")
    )

    class Meta:
        ordering = ["pk"]
        verbose_name = _("профиль")
        verbose_name_plural = _("профили")

    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True, verbose_name=_("адрес"))
    phone = models.CharField(max_length=12, validators=[regex_phone], verbose_name=_("номер телефона"))
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=_("баланс аккаунта"))

    def __str__(self):
        return self.user.username

class BrowsingHistory(models.Model):
    """История просмотров пользователя"""

    profile = models.ForeignKey(Profile, verbose_name=_("профиль"), related_name="goods", on_delete=models.PROTECT)
    goods = models.ManyToManyField("products.Product", related_name="goods", verbose_name=_("товары в истории"))
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("история просмотров")

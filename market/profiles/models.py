from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    """Роли пользователя"""

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    title = models.CharField(max_length=60, verbose_name=_("название"))
    description = models.CharField(max_length=200, verbose_name=_("описание"))

    def __str__(self):
        return self.title


class Profile(models.Model):
    """Профиль пользователя"""

    regex_phone = RegexValidator(
        regex=r"^((8|\+7|)(\d{10}))$",
        message="Формат номера телефона должен быть: +79999999999 или 89999999999"
    )

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True, verbose_name=_("адрес"))
    phone = models.CharField(max_length=12, validators=[regex_phone], verbose_name=_("номер телефона"))
    balance = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("баланс аккаунта"))

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


class BrowsingHistory(models.Model):
    """История просмотров пользователя"""

    user = models.ForeignKey(
        User,
        verbose_name=_("пользователь"),
        related_name="user",
        on_delete=models.PROTECT
    )
    products = models.ForeignKey(
        "products.Product",
        related_name="product",
        verbose_name=_("товары в истории"),
        on_delete=models.PROTECT
    )
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("история просмотров")

    def __str__(self):
        return f"History(pk={self.pk})"

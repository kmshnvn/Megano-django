from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    details = models.ManyToManyField("Detail", through="ProductDetail", verbose_name=_("характеристики"))
    description = models.CharField(blank=True, max_length=512, verbose_name=_("описание"))
    count = models.IntegerField(blank=True, verbose_name=_("количество"))
    preview = models.ImageField(blank=True, upload_to="products/preview")
    image = models.ImageField(blank=True, upload_to="products/image")
    # category = models.ManyToManyField("Category", null=True, verbose_name=_("категория"))

class Detail(models.Model):
    """Свойство продукта"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))


class ProductDetail(models.Model):
    """Значение свойства продукта"""

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    detail = models.ForeignKey(Detail, on_delete=models.PROTECT)
    value = models.CharField(max_length=128, verbose_name=_("значение"))
    # category = models.ForeignKey("Category", null=True, on_delete=models.PROTECT)

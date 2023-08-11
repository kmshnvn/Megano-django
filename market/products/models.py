from django.db import models
from django.utils.translation import gettext_lazy as _

# class Banner(models.Model):
#     def get_absolute_url(self):
#         return reverse('product', args=[Product.pk])
#
#     def get_product_image(self):
#         return Product.image


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    details = models.ManyToManyField("Detail", through="ProductDetail", verbose_name=_("характеристики"))
    description = models.CharField(max_length=512, verbose_name=_("описание"))
    preview = models.ImageField(blank=True, upload_to="products/preview")
    image = models.ImageField(blank=True, upload_to="products/image")
    # category = models.ManyToManyField("Category", null=True, verbose_name=_("категория"))

    class Meta:
        verbose_name = _("продукт")
        verbose_name_plural = _("продукты")

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"

    # def get_absolute_url(self):
    #     return f'/product/{self.pk}'


class Detail(models.Model):
    """Свойство продукта"""

    class Meta:
        verbose_name = _("характеристика")
        verbose_name_plural = _("характеристики")

    name = models.CharField(max_length=512, verbose_name=_("наименование"))

    def __str__(self) -> str:
        return f"Detail(pk={self.pk}, name={self.name!r})"


class ProductDetail(models.Model):
    """Значение свойства продукта"""

    class Meta:
        verbose_name = _("свойство продукта")
        verbose_name_plural = _("свойства продукта")

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    detail = models.ForeignKey(Detail, on_delete=models.PROTECT)
    value = models.CharField(max_length=128, verbose_name=_("значение"))
    # category = models.ForeignKey("Category", null=True, on_delete=models.PROTECT)

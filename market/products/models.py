from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _

# class Banner(models.Model):
#     def get_absolute_url(self):
#         return reverse('product', args=[Product.pk])
#
#     def get_product_image(self):
#         return Product.image


class Category(MPTTModel):
    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.CharField(max_length=512, verbose_name=_("описание"))
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Родительская категория',
        related_name="children",
        on_delete=models.PROTECT,
    )

    class MPTTMeta:
        order_insertion_by = ("name",)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'products_categories'

    def __str__(self) -> str:
        return f"Category(pk={self.pk}, name={self.name!r})"


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    details = models.ManyToManyField("Detail", through="ProductDetail", verbose_name=_("характеристики"))
    description = models.CharField(max_length=512, verbose_name=_("описание"))
    preview = models.ImageField(blank=True, upload_to="products/preview")
    image = models.ImageField(blank=True, upload_to="products/image")
    category = models.ForeignKey(
        Category, verbose_name=_("категория"),
        related_name="products",
        on_delete=models.PROTECT
    )

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
    category = TreeForeignKey(Category, on_delete=models.PROTECT)

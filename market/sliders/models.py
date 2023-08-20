from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product


def slider_upload_path(instance: "Slider", filename: str) -> str:
    return "sliders/image/{instance_name}_{filename}".format(instance_name=instance.title, filename=filename)


class Slider(models.Model):
    """Модель слайдер"""

    class Meta:
        verbose_name = _("слайдер")
        verbose_name_plural = _("слайдеры")

    title = models.CharField(max_length=200, verbose_name=_("заголовок"))
    description = models.CharField(max_length=400, verbose_name=_("описание"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="slider", verbose_name=_("продукт"))
    image = models.ImageField(upload_to=slider_upload_path, verbose_name=_("изображение слайдера"))

    def __str__(self):
        return f"Слайдер: {self.title}"

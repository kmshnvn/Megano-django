from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from products.models import Product
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    """
    Модель отзыва о продукте.
    В модели прописано 2 дополнительных метода,
    которые возвращают статистические данные.
    """

    class Meta:
        ordering = ["date_publish"]
        verbose_name = _("отзыв")
        verbose_name_plural = _("отзывы")

    author: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", verbose_name=_("пользователь")
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments", verbose_name=_("продукт"))
    text = models.TextField(max_length=600, blank=True, verbose_name=_("текст отзыва"))
    date_publish = models.DateTimeField(auto_now=True, verbose_name=_("дата публикации"))

    def __str__(self) -> str:
        return f"Отзыв {self.author.username} о продукте {self.product.name}"

    @classmethod
    def get_number_comments(cls, product_pk: int) -> int:
        """
        Метод получения количества отзывов для товара.

        :param product_pk: Передает pk модели Product.
        :return count: Число отзывов.
        """

        count = cls.objects.filter(product_id=product_pk).count()
        return count

    @classmethod
    def get_list_comments(cls, product_pk: int, offset: int = 0, limit: int = 10) -> QuerySet:
        """
        Метод получения список отзывов к товару.
        Принимает pk модели Product, а также смещения и лимит возвращаемого результата.

        :param product_pk: Передает pk модели Product.
        :param offset: Передает количество записей, которые необходимо пропустить.
        :param limit: Передает лимит записей, которые необходимо извлечь.
        :return: QuerySet, Список отзывов о товаре.
        """

        comments = cls.objects.select_related("author", "product").filter(product_id=product_pk)[offset:limit]
        return comments

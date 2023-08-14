from comments.forms import CommentAddForm
from comments.models import Comment
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.db.models import Min
from django.views.generic.edit import FormMixin
from shops.models import (
    Offer,
)
from .models import (
    ProductDetail,
    Product,
)


class ProductDetailViev(FormMixin, View):
    form_class = CommentAddForm
    context = {}

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        offers = Offer.objects.prefetch_related("shop").filter(product_id=pk)
        product_details = ProductDetail.objects.prefetch_related("detail", "product").get(product_id=pk)

        comments = Comment.get_list_comments(product_pk=pk)
        comment_count = Comment.get_number_comments(product_pk=pk)

        self.context = {
            "offers": offers,
            "product": product_details.product,
            "product_detail": product_details,
            "min_price": offers.aggregate(Min("price"))["price__min"],
            "comments_list": comments,
            "comment_count": comment_count,
        }
        return render(request, "products/product-detail.jinja2", context=self.context)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Принимаем данные формы, сохраняем новый отзыв в БД."""

        form = CommentAddForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(pk=pk)

            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.product = product
            new_comment.save()
            return self.form_valid(form)

        self.context["form"] = form
        return render(request, "products/product-detail.jinja2", context=self.context)

    def get_success_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.kwargs["pk"]})

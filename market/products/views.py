from comments.forms import CommentAddForm
from comments.models import Comment
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Min
from django.views.generic.edit import CreateView
from shops.models import (
    Offer,
)
from .models import (
    ProductDetail,
    Product,
)


class ProductDetailViev(CreateView):
    form_class = CommentAddForm
    template_name = "products/product-detail.jinja2"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        pk = kwargs["pk"]
        offers = Offer.objects.prefetch_related("shop").filter(product_id=pk)
        product_details = ProductDetail.objects.prefetch_related("detail", "product").get(product_id=pk)

        comments = Comment.get_list_comments(product_pk=pk)
        comment_count = Comment.get_number_comments(product_pk=pk)

        context = {
            "offers": offers,
            "product": product_details.product,
            "product_detail": product_details,
            "min_price": offers.aggregate(Min("price"))["price__min"],
            "comments_list": comments,
            "comment_count": comment_count,
        }
        return render(request, "products/product-detail.jinja2", context=context)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.product = Product.objects.get(pk=self.kwargs["pk"])
        comment.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.kwargs["pk"]})

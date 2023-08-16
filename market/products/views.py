from comments.forms import CommentAddForm
from comments.models import Comment
from django.http import Http404
from django.urls import reverse
from django.db.models import Min
from django.views.generic.edit import CreateView
from shops.models import (
    Offer,
)
from .models import (
    ProductDetail,
    Product,
)


class ProductDetailVieW(CreateView):
    form_class = CommentAddForm
    template_name = "products/product-detail.jinja2"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        pk = self.kwargs["pk"]
        offers = Offer.objects.prefetch_related("shop").filter(product_id=pk)
        try:
            product_details = ProductDetail.objects.prefetch_related("detail", "product").get(product_id=pk)

        except ProductDetail.DoesNotExist:
            raise Http404(f"Продукт под номером {pk}, отсутствует в базе данных")

        comments = Comment.get_list_comments(product_pk=pk)
        comment_count = Comment.get_number_comments(product_pk=pk)

        data["offers"] = offers
        data["product"] = product_details
        data["min_price"] = offers.aggregate(Min("price"))["price__min"]
        data["comments_list"] = comments
        data["comment_count"] = comment_count

        return data

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.product = Product.objects.get(pk=self.kwargs["pk"])
        comment.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.kwargs["pk"]})

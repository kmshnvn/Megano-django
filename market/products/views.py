# from comments.forms import CommentAddForm
# from comments.models import Comment
# from django.http import Http404
# from django.urls import reverse
# from django.db.models import Min
# from django.views.generic import DetailView
# from django.views.generic.edit import FormMixin
# from shops.models import (
#     Offer,
# )
# from .models import (
#     ProductDetail,
#     Product,
# )
#
#
# class ProductDetailView(FormMixin, DetailView):
#     model = Product
#     form_class = CommentAddForm
#     template_name = "products/product-detail.jinja2"
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#
#         offers = Offer.objects.prefetch_related("shop").filter(product_id=self.object.pk)
#         try:
#             product_details = ProductDetail.objects.prefetch_related("detail", "product").get(product_id=self.object.pk)
#         except ProductDetail.DoesNotExist:
#             raise Http404(f"Продукт под номером {self.object.id}, отсутствует в базе данных")
#
#         comments = Comment.objects.select_related("author", "product").filter(product_id=self.object.pk)[:10]
#         comment_count = Comment.objects.filter(product_id=self.object.pk).count()
#
#         data["offers"] = offers
#         data["product"] = product_details.product
#         data["product_detail"] = product_details
#         data["min_price"] = offers.aggregate(Min("price"))["price__min"]
#         data["comments_list"] = comments
#         data["comment_count"] = comment_count
#
#         return data
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         comment = form.save(commit=False)
#         comment.author = self.request.user
#         comment.product = Product.objects.get(pk=self.kwargs["pk"])
#         comment.save()
#
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse("products:product_detail", kwargs={"pk": self.object.id})
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.db.models import Min
from shops.models import (
    Offer,
)
from .models import (
    ProductDetail,
Product
)
from basket.forms import BasketAddProductForm
from basket.basket import BasketObject

class ProductDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        offers = Offer.objects.prefetch_related("shop").filter(product_id=pk)
        product_details = ProductDetail.objects.prefetch_related("detail", "product").get(product_id=pk)
        form = BasketAddProductForm
        context = {
            "offers": offers,
            "product": product_details.product,
            "product_detail": product_details,
            "min_price": offers.aggregate(Min("price"))["price__min"],
            "form": form
        }
        return render(request, "products/product-detail.jinja2", context=context)

    def post(self, request: HttpRequest, pk:int):
        product = get_object_or_404(Product, pk=pk)
        basket = BasketObject(request=request)
        form = BasketAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            basket.add_product(
                request=request,
                product=product,
                     amount=cd["amount"],
            )

        return redirect(to="products:product_detail", pk=self.object.pk)
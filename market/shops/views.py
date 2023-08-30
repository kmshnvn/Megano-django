from django.db.models import Count, QuerySet
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from products.models import Product
from shops.forms import CatalogFiltersForm


class CatalogListView(FormMixin, ListView):
    """Класс представления каталога товаров"""

    form_class = CatalogFiltersForm
    template_name = "shops/catalog.jinja2"
    context_object_name = "products"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get("cat", None):
            context["cat"] = self.kwargs["cat"]

        if self.kwargs.get("sort", None):
            context["products"] = self.sort_products(product=context["products"], key=self.kwargs["sort"])

        return context

    def get_queryset(self):
        print(self.kwargs)
        product = Product.objects.prefetch_related("category", "offers")

        if self.kwargs.get("cat", None) and self.request.method == "GET":  # возвращаем товары по категориям
            product = product.filter(category__name=self.kwargs["cat"])

        # if self.request.method == "POST":  # фильтрация товаров
        form = CatalogFiltersForm(self.request.POST)

        if form.is_valid():
            price_from, price_to = form.cleaned_data.get("price")
            name = form.cleaned_data.get("title", "")

            product = product.filter(offers__price__range=(price_from, price_to)).filter(name__icontains=name)

            if form.cleaned_data.get("available", None):
                product = product.filter(offers__remainder__gt=0)

            if self.kwargs.get("cat", None):  # возвращаем товары по категориям
                product = product.filter(category__name=self.kwargs["cat"])

        return product

    def sort_products(self, product: QuerySet, key: str) -> QuerySet:
        """Метод сортировки товаров по заданному ключу"""

        if key == "price":
            return product.order_by("offers__price")

        if key == "comments":
            return product.annotate(count=Count("comments")).order_by("count")

        if key == "date":
            return product.order_by("date_added")

        if key == "popular":
            pass

        return product

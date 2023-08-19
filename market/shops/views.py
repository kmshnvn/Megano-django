from django.views.generic import ListView
from products.models import Product


class CatalogListView(ListView):
    model = Product
    template_name = "shops/catalog.jinja2"
    context_object_name = "products"

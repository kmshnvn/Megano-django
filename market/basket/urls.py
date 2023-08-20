from django.urls import path
from .views import BasketView, add_product


app_name = "basket"

urlpatterns = [
    path("", BasketView.as_view(), name="basket_view"),
    path("add_product/<int:product_pk>", add_product, name="add_random_product"),
    path("add_product/<int:product_pk>/<int:offer_pk>", add_product, name="add_product"),
]
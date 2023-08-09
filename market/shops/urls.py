from django.urls import path
from .views import ProductDetailViev


app_name = "shop"

urlpatterns = [
    path("products/<int:pk>/", ProductDetailViev.as_view(), name="product_detail"),
]

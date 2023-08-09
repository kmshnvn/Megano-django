from django.urls import path, include
from .views import ProductDetailViev


app_name = "shop"

urlpatterns = [
    path("products/<int:pk>/", ProductDetailViev.as_view(), name="product_detail"),
]
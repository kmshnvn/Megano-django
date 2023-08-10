from django.urls import path
from .views import ProductDetailViev


app_name = "products"

urlpatterns = [
    path("details/<int:pk>/", ProductDetailViev.as_view(), name="product_detail"),
]

from django.urls import path
from .views import ProductDetailViev


app_name = "products"

urlpatterns = [
    path("<int:pk>/", ProductDetailViev.as_view(), name="product_detail"),
]

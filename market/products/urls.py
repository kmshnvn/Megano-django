from django.urls import path
from .views import ProductDetailVieW


app_name = "products"

urlpatterns = [
    path("<int:pk>/", ProductDetailVieW.as_view(), name="product_detail"),
]

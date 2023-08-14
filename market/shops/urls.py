from django.urls import path
from .views import ShopDetailView


app_name = "shops"

urlpatterns = [
    path("<int:pk>/", ShopDetailView.as_view(), name="shop_detail"),
]

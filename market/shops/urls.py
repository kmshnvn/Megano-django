from django.urls import path
from .views import CatalogListView

app_name = "shops"

urlpatterns = [
    path("catalog/", CatalogListView.as_view(), name="catalog"),
]

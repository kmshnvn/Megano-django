from django.urls import path
from .views import CatalogListView

app_name = "shops"

urlpatterns = [
    path("catalog/", CatalogListView.as_view(), name="shops-catalog"),
    path("catalog/<str:cat>/", CatalogListView.as_view(), name="shops-catalog"),
    path("catalog/sort/<str:sort>/", CatalogListView.as_view(), name="shops-catalog"),
    path("catalog/<str:cat>/sort/<str:sort>/", CatalogListView.as_view(), name="shops-catalog"),
]

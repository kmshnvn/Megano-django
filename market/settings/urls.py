from django.urls import path
from settings.views import clear_all_cache_view

app_name = 'settings'

urlpatterns = [
    path('', clear_all_cache_view, name='clear_all_cache'),
]

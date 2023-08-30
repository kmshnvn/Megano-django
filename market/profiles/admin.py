from django.contrib import admin
from .models import BrowsingHistory, Profile


@admin.register(BrowsingHistory)
class HistoryAdmin(admin.ModelAdmin):
    list_display = "pk", "date"
    list_display_links = "pk", "date"

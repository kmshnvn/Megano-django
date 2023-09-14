from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "user", "phone", "balance"
    list_display_links = "user", "phone", "balance"

from django.contrib import admin
from profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = "user", "address", "phone", "balance"
    list_display_links = "user", "address", "phone", "balance"


# Register your models here.

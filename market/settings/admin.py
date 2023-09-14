from django.contrib import admin
from settings.models import Settings
from django.db.utils import ProgrammingError


class SettingsAdmin(admin.ModelAdmin):

    change_form_template = "settings/settings.jinja2"

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        try:
            Settings.load().save()
        except ProgrammingError:
            pass

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


admin.register(Settings, SettingsAdmin)

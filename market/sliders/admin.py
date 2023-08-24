from django.contrib import admin
from sliders.models import Slider


class SliderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "product",
        "image",
    )
    list_filter = (
        "id",
        "title",
    )


admin.site.register(Slider, SliderAdmin)

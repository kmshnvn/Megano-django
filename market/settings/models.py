from django.db import models
from settings.singleton_model import SingletonModel


class Settings(SingletonModel):
    class Meta:
        verbose_name_plural = 'settings'
        verbose_name = 'settings'

    def __str__(self) -> str:
        return "site_settings"

    product_cache_time = models.PositiveIntegerField(default=1, verbose_name='Дней кэширования продукта')
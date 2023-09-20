from order.models import OrderStatus
from django.core.management import BaseCommand
from django.db import transaction


ORDER_STATUS_NAMES = ["создан", "оплачен", "доставляется", "завершен", "отменен"]


class Command(BaseCommand):
    """Команда для создания статусов заказов"""

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Создаем статусы заказа...")
        for status in ORDER_STATUS_NAMES:
            OrderStatus.objects.create(name=status)
        self.stdout.write("Успешно создано!")

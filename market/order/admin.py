from django.contrib import admin
from order.models import Order, Delivery, OrderStatus, ProductInOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "user", "customer", "date_added", "email", "phone", "order_status", "delivery"
    list_display_links = "user", "customer", "date_added", "email", "phone", "order_status", "delivery"


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = "delivery_type", "city", "address", "pay"
    list_display_links = "delivery_type", "city", "address", "pay"


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)


@admin.register(ProductInOrder)
class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = "product", "order", "price", "amount"
    list_display_links = "product", "order", "price", "amount"

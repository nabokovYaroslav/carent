from django.contrib import admin

from orders.models import Order
from orders.forms import OrderForm


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm

admin.site.register(Order, OrderAdmin)
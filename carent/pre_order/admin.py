from django.contrib import admin

from pre_order.models import PreOrder
from pre_order.forms import PreOrderForm


class PreOrderAdmin(admin.ModelAdmin):
    form = PreOrderForm

admin.site.register(PreOrder, PreOrderAdmin)
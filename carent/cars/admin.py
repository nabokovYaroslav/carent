from django.contrib import admin
from eav.forms import BaseDynamicEntityForm
from eav.admin import BaseEntityAdmin

from cars.models import Car, Brand, CarImage


class CarAdminForm(BaseDynamicEntityForm):
    model = Car

class CarAdmin(BaseEntityAdmin):
    form = CarAdminForm



admin.site.register(Car, CarAdmin)
admin.site.register(Brand)
admin.site.register(CarImage)
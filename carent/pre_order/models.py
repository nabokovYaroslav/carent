import re

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from cars.models import Car


PHONE_REG = r'^(\+375|80)(29|25|44|33)\d{7}$'

def validate_phone(value):

    if not re.search(PHONE_REG, value):
        raise ValidationError(
            _('%(value)s is not a valid value. Phone should be in format (+375|80)(29|25|44|33)XXXXXXX'),
            params={'value': value},
        )

class PreOrder(models.Model):

    STATUS_CHOICES = [
        ("completed", "Звонок совершен"),
        ("not_completed", "Звонок не совершен"),
    ]

    name = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.CharField(max_length=13, verbose_name="Телефон", validators=[validate_phone])
    car = models.ForeignKey(Car, verbose_name="Машина", on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="Статус", default="not_completed", blank=True)

    def __str__(self):
        return "№{} {} {}".format(self.id, self.name, self.phone)

    class Meta:
        verbose_name = 'Предзаказ'
        verbose_name_plural = 'Предзаказы'
import re

from django.forms import Field, ModelForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from pre_order.models import PreOrder


class PhoneFormField(Field):
    message = _('Phone should be in format (+375|80)(29|25|44|33)XXXXXXX where X is number')
    code = 'invalid'
    PHONE_REG = r'^(\+375|80)(29|25|44|33)\d{7}$'

    def validate(self, value):
        super().validate(value)
        if not re.search(self.PHONE_REG, value):
            raise ValidationError(self.message, self.code)

class PreOrderForm(ModelForm):
    phone = PhoneFormField(label="Телефон")
    class Meta:
        model = PreOrder
        fields = '__all__'
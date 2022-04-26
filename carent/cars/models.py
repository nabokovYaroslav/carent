import os

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from eav.decorators import register_eav
from eav.registry import EavConfig

from utils.image import (change_resolution, create_adaptive_resolution_image, compare_images, 
                        create_adaptive_format_image, create_tumbnail_image, delete_images)

class CarConfig(EavConfig):

    @classmethod
    def get_attributes(cls, instance=None):
        return super().get_attributes(instance).filter(value__entity_id=instance.id)

def validate_discount(value):
    if value > 100:
        raise ValidationError(
            _('%(value)s is not a valid value. Discount cannot be more than 100%'),
            params={'value': value},
        )


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Марка автомобиля")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'

@register_eav(config_cls=CarConfig)
class Car(models.Model):

    def upload_to(self, file):
        name, ext = os.path.splitext(file)
        path = "images/cars/"
        datetime = timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        output_path = '{}{}-{}{}'.format(path, name, datetime, ext)
        return output_path

    name = models.CharField(max_length=255, verbose_name="Название автомобиля")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Марка")
    price = models.PositiveIntegerField(verbose_name="Цена")
    discount = models.PositiveSmallIntegerField(verbose_name="Скидка", validators=[validate_discount])
    image = models.ImageField(verbose_name="Фотография", upload_to=upload_to)

    def __str__(self):
        return "{id} {brand} {name}".format(id=self.id, brand=self.brand, name=self.name)

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        try:
            instance = Car.objects.get(id=self.id)
        except Car.DoesNotExist:
            instance = None
        if instance is not None:
            if not compare_images(instance.image.path, self.image):
                delete_images(instance.image.path)
                self.image = change_resolution(self.image)
        else:
            self.image = change_resolution(self.image)
        super().save(*args, **kwargs)
        create_adaptive_resolution_image(self.image.path, formatting=True)
        create_adaptive_format_image(self.image.path)
        create_tumbnail_image(self.image.path, formatting=True)

    @property
    def price_with_discount(self):
        return int(self.price - self.price * self.discount / 100)

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

class CarImage(models.Model):
    def upload_to(self, file):
        name, ext = os.path.splitext(file)
        path = "images/cars/"
        datetime = timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        output_path = '{}{}-{}{}'.format(path, name, datetime, ext)
        return output_path

    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Машина")
    image = models.ImageField(verbose_name="Фотография", upload_to=upload_to)

    def __str__(self):
        return str(self.car)

    def save(self, *args, **kwargs):
        try:
            instance = CarImage.objects.get(id=self.id)
        except CarImage.DoesNotExist:
            instance = None
        if instance is not None:
            if instance.image != self.image:
                delete_images(instance.image.path)
                self.image = change_resolution(self.image)
        else:
            self.image = change_resolution(self.image)
        super().save(*args, **kwargs)
        create_adaptive_resolution_image(self.image.path, formatting=True)
        create_adaptive_format_image(self.image.path)
        create_tumbnail_image(self.image.path, formatting=True)

    class Meta:
        verbose_name = 'Фото машины'
        verbose_name_plural = 'Фото машин'
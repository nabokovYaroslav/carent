from django.db.models.signals import post_delete
from django.dispatch import receiver

from cars.models import Car, CarImage
from utils.image import delete_images


@receiver(post_delete, sender=Car)
def car_delete_images(sender, **kwargs):
  instance = kwargs["instance"]
  delete_images(instance.image.path)

@receiver(post_delete, sender=CarImage)
def car_image_delete_images(sender, **kwargs):
  instance = kwargs["instance"]
  delete_images(instance.image.path)
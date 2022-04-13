from django.apps import AppConfig


class CarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cars'
    verbose_name = "Машины"

    def ready(self):
        from cars.signals import car_delete_images, car_image_delete_images
        return super().ready()
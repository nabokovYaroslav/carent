from django.apps import AppConfig


class PreOrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pre_order'
    verbose_name = "Заказы"
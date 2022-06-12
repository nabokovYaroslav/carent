from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eav'
    verbose_name = "Сущность-Атрибут-Значение"
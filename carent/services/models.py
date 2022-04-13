from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Название услуги")
    text = models.TextField(verbose_name="Описание услуги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
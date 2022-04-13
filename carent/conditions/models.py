from django.db import models


class Condition(models.Model):
    description = models.CharField(max_length=255, verbose_name="Описание условия")

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = 'Условие проката'
        verbose_name_plural = 'Условия проката'
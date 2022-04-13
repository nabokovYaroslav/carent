# Generated by Django 3.2.12 on 2022-04-12 14:15

from django.db import migrations, models
import django.db.models.deletion
import orders.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0004_carimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('phone', models.CharField(max_length=13, validators=[orders.models.validate_phone], verbose_name='Телефон')),
                ('day', models.PositiveSmallIntegerField(verbose_name='Кол-во дней')),
                ('cost', models.PositiveIntegerField(verbose_name='Стоимость')),
                ('status', models.CharField(blank=True, choices=[('completed', 'Звонок совершен'), ('not_completed', 'Звонок не совершен')], default='not_completed', max_length=50, verbose_name='Статус')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.car', verbose_name='Машина')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]

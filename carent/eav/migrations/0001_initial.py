# Generated by Django 2.0.4 on 2018-06-01 09:36

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import eav.fields


class Migration(migrations.Migration):
    """Initial migration that creates the Attribute, EnumGroup, EnumValue, and Value models."""

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='User-friendly attribute name',
                        max_length=100,
                        verbose_name='Name',
                    ),
                ),
                (
                    'slug',
                    eav.fields.EavSlugField(
                        help_text='Short unique attribute label',
                        unique=True,
                        verbose_name='Slug',
                    ),
                ),
                (
                    'description',
                    models.CharField(
                        blank=True,
                        help_text='Short description',
                        max_length=256,
                        null=True,
                        verbose_name='Description',
                    ),
                ),
                (
                    'datatype',
                    eav.fields.EavDatatypeField(
                        choices=[
                            ('text', 'Text'),
                            ('date', 'Date'),
                            ('float', 'Float'),
                            ('int', 'Integer'),
                            ('bool', 'True / False'),
                            ('object', 'Django Object'),
                            ('enum', 'Multiple Choice'),
                        ],
                        max_length=6,
                        verbose_name='Data Type',
                    ),
                ),
                (
                    'created',
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='Created',
                    ),
                ),
                (
                    'modified',
                    models.DateTimeField(auto_now=True, verbose_name='Modified'),
                ),
                (
                    'required',
                    models.BooleanField(default=False, verbose_name='Required'),
                ),
                (
                    'display_order',
                    models.PositiveIntegerField(
                        default=1, verbose_name='Display order'
                    ),
                ),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='EnumGroup',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=100, unique=True, verbose_name='Name'),
                ),
            ],
        ),
        migrations.CreateModel(
            name='EnumValue',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'value',
                    models.CharField(
                        db_index=True, max_length=50, unique=True, verbose_name='Value'
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('entity_id', models.IntegerField()),
                ('value_text', models.TextField(blank=True, null=True)),
                ('value_float', models.FloatField(blank=True, null=True)),
                ('value_int', models.IntegerField(blank=True, null=True)),
                ('value_date', models.DateTimeField(blank=True, null=True)),
                ('value_bool', models.NullBooleanField()),
                ('generic_value_id', models.IntegerField(blank=True, null=True)),
                (
                    'created',
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name='Created'
                    ),
                ),
                (
                    'modified',
                    models.DateTimeField(auto_now=True, verbose_name='Modified'),
                ),
                (
                    'attribute',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to='eav.Attribute',
                        verbose_name='Attribute',
                    ),
                ),
                (
                    'entity_ct',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='value_entities',
                        to='contenttypes.ContentType',
                    ),
                ),
                (
                    'generic_value_ct',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='value_values',
                        to='contenttypes.ContentType',
                    ),
                ),
                (
                    'value_enum',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='eav_values',
                        to='eav.EnumValue',
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='enumgroup',
            name='values',
            field=models.ManyToManyField(to='eav.EnumValue', verbose_name='Enum group'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='enum_group',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='eav.EnumGroup',
                verbose_name='Choice Group',
            ),
        ),
    ]

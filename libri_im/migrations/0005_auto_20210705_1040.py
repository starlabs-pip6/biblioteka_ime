# Generated by Django 3.2.4 on 2021-07-05 08:40

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libri_im', '0004_auto_20210705_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='read',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=[], null=True, size=None),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='reading',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=[], null=True, size=None),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='want_to_read',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=[], null=True, size=None),
        ),
    ]
# Generated by Django 3.2.4 on 2021-07-05 08:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libri_im', '0006_auto_20210705_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='read',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, null=True, size=None),
        ),
    ]

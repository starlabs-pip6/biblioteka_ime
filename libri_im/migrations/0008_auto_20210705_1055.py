# Generated by Django 3.2.4 on 2021-07-05 08:55

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libri_im', '0007_alter_newuser_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='reading',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='want_to_read',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, null=True, size=None),
        ),
    ]

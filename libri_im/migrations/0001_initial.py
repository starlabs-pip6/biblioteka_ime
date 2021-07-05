# Generated by Django 3.2.4 on 2021-07-05 07:23

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('hide_email', models.BooleanField(default=True)),
                ('read', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('want_to_read', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('reading', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id_libri', models.AutoField(primary_key=True, serialize=False)),
                ('isbn', models.BigIntegerField()),
                ('titulli', models.CharField(max_length=500)),
                ('autori', models.CharField(max_length=100)),
                ('kategoria', models.CharField(max_length=100)),
                ('pershkrimi', models.TextField()),
                ('mes_vleresimit', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nr_vleresimit', models.IntegerField()),
                ('nr_faqeve', models.IntegerField()),
                ('viti_publikimit', models.IntegerField()),
                ('image_link', models.CharField(default='https://www.directtextbook.com/large/.jpg', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pages_now', models.IntegerField(default=0)),
                ('id_libri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libri_im.book')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

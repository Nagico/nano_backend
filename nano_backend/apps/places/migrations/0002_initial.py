# Generated by Django 3.2.5 on 2021-12-24 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='contributor',
            field=models.ManyToManyField(related_name='place_contributor', to=settings.AUTH_USER_MODEL, verbose_name='贡献者'),
        ),
        migrations.AddField(
            model_name='place',
            name='create_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place_create_user', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
    ]

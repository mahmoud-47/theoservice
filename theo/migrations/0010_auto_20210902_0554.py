# Generated by Django 3.1.5 on 2021-09-02 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('theo', '0009_auto_20210901_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commande',
            name='contact',
        ),
        migrations.AddField(
            model_name='commande',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Panier',
        ),
    ]
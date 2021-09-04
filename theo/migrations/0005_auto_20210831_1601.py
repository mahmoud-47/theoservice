# Generated by Django 3.1.5 on 2021-08-31 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('theo', '0004_produit_prix'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='prenom',
        ),
        migrations.AddField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte', models.IntegerField(default=1)),
                ('commanded', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theo.produit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

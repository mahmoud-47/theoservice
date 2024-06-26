# Generated by Django 3.1.5 on 2021-08-31 22:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theo', '0005_auto_20210831_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=30)),
                ('nom', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('message', models.TextField(blank=True, max_length=150, validators=[django.core.validators.MaxLengthValidator(150)])),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

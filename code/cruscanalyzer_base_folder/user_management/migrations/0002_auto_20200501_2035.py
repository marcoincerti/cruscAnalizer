# Generated by Django 3.0.5 on 2020-05-01 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utente',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
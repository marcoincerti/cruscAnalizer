# Generated by Django 3.0.6 on 2020-05-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_management', '0008_auto_20200520_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertextsettings',
            name='blacklist_string',
            field=models.TextField(default=''),
        ),
    ]

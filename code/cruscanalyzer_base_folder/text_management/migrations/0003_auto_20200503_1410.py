# Generated by Django 3.0.5 on 2020-05-03 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_management', '0002_auto_20200503_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='category',
        ),
        migrations.AddField(
            model_name='text',
            name='category',
            field=models.ManyToManyField(related_name='category', to='text_management.Category'),
        ),
    ]

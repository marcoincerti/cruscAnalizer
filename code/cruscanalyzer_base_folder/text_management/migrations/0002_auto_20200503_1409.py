# Generated by Django 3.0.5 on 2020-05-03 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('text_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='category',
        ),
        migrations.AddField(
            model_name='text',
            name='category',
            field=models.ForeignKey(null='true', on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='text_management.Category'),
            preserve_default='true',
        ),
    ]

# Generated by Django 2.2.3 on 2019-07-21 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weightapp', '0004_weightapp_myweight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weightapp',
            name='Myweight',
        ),
    ]

# Generated by Django 4.0 on 2021-12-14 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_stocks'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stocks',
            new_name='Stock',
        ),
    ]

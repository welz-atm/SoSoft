# Generated by Django 3.0.6 on 2020-06-08 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_remove_warehouse_warehouse'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Stock',
        ),
    ]

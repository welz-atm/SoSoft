# Generated by Django 3.0.6 on 2020-06-08 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20200608_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='warehouse',
            field=models.ManyToManyField(to='product.WarehouseItem'),
        ),
    ]

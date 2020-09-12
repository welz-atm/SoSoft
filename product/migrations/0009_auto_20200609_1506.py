# Generated by Django 3.0.6 on 2020-06-09 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_warehouseitem_warehouse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouseitem',
            name='received',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='warehouseitem',
            name='supplied',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

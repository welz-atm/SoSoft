# Generated by Django 3.0.6 on 2020-06-08 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200530_2232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='warehouse',
            old_name='created_by',
            new_name='owner',
        ),
    ]
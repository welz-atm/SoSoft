# Generated by Django 3.0.6 on 2020-06-19 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20200617_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.IntegerField(blank=True, default=3500, null=True),
        ),
    ]

# Generated by Django 3.0.6 on 2020-07-20 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0005_auto_20200709_1858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distributordept',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='distributordept',
            name='created_by',
        ),
        migrations.AddField(
            model_name='customuser',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authenticate.SalesDept'),
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-06 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='budget',
            name='title',
            field=models.CharField(default='Budget Title', max_length=50),
        ),
        migrations.AddField(
            model_name='transaction',
            name='budget',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tenants.budget'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='title',
            field=models.CharField(default='Transaction Title', max_length=50),
        ),
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(null=True),
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-11 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0005_alter_budget_date_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.CharField(default='None', max_length=50, null=True),
        ),
    ]

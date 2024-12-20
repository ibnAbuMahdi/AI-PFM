# Generated by Django 5.1.2 on 2024-11-07 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0003_budget_date_alter_transaction_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='budget',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='tenants.budget'),
        ),
    ]

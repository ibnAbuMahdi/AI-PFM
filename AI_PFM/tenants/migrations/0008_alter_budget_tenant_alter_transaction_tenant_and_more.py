# Generated by Django 5.1.2 on 2025-02-16 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0007_alter_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tenants.tenant'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tenants.tenant'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tenants.tenant'),
        ),
    ]

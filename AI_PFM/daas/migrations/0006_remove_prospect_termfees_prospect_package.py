# Generated by Django 5.1.2 on 2025-02-20 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daas', '0005_prospect_address_prospect_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prospect',
            name='termfees',
        ),
        migrations.AddField(
            model_name='prospect',
            name='package',
            field=models.TextField(null=True),
        ),
    ]

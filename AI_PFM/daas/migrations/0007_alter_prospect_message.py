# Generated by Django 5.1.2 on 2025-03-02 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daas', '0006_remove_prospect_termfees_prospect_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prospect',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]

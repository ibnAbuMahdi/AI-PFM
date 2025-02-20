# Generated by Django 5.1.2 on 2025-02-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daas', '0004_alter_prospect_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='prospect',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='prospect',
            name='message',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='prospect',
            name='stage',
            field=models.CharField(choices=[('cont', 'Contact'), ('disc', 'Discussion'), ('app', 'Appointment'), ('dec', 'Decision'), ('agr', 'Agreement')], default='cont', max_length=20),
        ),
    ]

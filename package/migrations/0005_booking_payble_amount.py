# Generated by Django 5.1.4 on 2024-12-18 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0004_alter_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payble_amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
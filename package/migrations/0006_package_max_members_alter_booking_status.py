# Generated by Django 5.1.4 on 2024-12-18 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0005_booking_payble_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='max_members',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]

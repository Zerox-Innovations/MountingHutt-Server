# Generated by Django 5.1.4 on 2024-12-25 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0002_booking_razorpay_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

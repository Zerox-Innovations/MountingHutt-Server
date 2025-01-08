# Generated by Django 5.1.4 on 2025-01-07 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0002_rename_booking_date_booking_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='first_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='last_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='pro_noun',
            field=models.CharField(blank=True, choices=[('Mr', 'Mr'), ('Mrs', 'mrs')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='razorpay_order_id',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='zip_code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='banner_image',
            field=models.ImageField(blank=True, null=True, upload_to='package'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='contact_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]

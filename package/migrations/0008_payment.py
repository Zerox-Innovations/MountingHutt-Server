# Generated by Django 5.1.4 on 2024-12-18 10:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0007_rename_payble_amount_booking_advance_amount_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_amount', models.PositiveIntegerField()),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('booking_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_data', to='package.booking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paid_customuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
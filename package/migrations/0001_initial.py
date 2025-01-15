

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=500)),
                ('days', models.PositiveIntegerField(default=1)),
                ('nights', models.PositiveIntegerField(default=1)),
                ('min_members', models.PositiveBigIntegerField(blank=True, null=True)),
                ('max_members', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.PositiveIntegerField()),
                ('additional_info', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PackageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(choices=[('banner', 'Banner Image'), ('background', 'Background Image'), ('thumbnail', 'Thumbnail Image'), ('gallery', 'Gallery Image')], default='gallery', max_length=50)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='package.package')),
            ],
        ),
        migrations.CreateModel(
            name='DayDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_number', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day_details', to='package.package')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('travel_start_date', models.DateField()),
                ('travel_end_date', models.DateField()),
                ('number_of_travelers', models.PositiveIntegerField(default=1)),
                ('total_amount', models.PositiveIntegerField()),
                ('payable_amount', models.PositiveIntegerField(blank=True, null=True)),
                ('advance_amount', models.PositiveIntegerField()),
                ('balance_amount', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Confirmed', 'Confirmed'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('first_name', models.CharField(blank=True, max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=15, null=True)),
                ('pro_noun', models.CharField(blank=True, choices=[('Mr', 'Mr'), ('Mrs', 'mrs')], max_length=20, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('razorpay_order_id', models.CharField(blank=True, null=True)),

                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customuser', to=settings.AUTH_USER_MODEL)),
                ('booking_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package', to='package.package')),

            ],
        ),
    ]

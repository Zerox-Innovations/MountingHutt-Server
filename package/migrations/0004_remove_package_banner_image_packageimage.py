# Generated by Django 5.1.4 on 2025-01-09 06:59

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0003_delete_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='banner_image',
        ),
        migrations.CreateModel(
            name='PackageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='package.package')),
            ],
        ),
    ]

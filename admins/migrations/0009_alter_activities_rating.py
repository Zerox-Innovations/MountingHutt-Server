# Generated by Django 5.1.4 on 2024-12-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0008_alter_item_category_food_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='rating',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

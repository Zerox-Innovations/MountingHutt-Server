# Generated by Django 5.1.4 on 2024-12-19 08:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0004_alter_food_category_food_item_alter_food_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_time', models.CharField(max_length=250)),
            ],
        ),
        migrations.RemoveField(
            model_name='food',
            name='item',
        ),
        migrations.AddField(
            model_name='food',
            name='item_time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foodtime', to='admins.item_category'),
        ),
    ]
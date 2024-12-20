# Generated by Django 5.1.4 on 2024-12-19 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_alter_foodcategory_breakfast_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.CharField(blank=True, choices=[('veg', 'veg'), ('Non-Veg', 'Non-Veg'), ('Hot', 'Hot'), ('Cool', 'Cool')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='item',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='rating',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.DeleteModel(
            name='FoodCategory',
        ),
    ]

# Generated by Django 5.1.4 on 2024-12-20 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0009_alter_activities_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='title',
            new_name='item',
        ),
    ]
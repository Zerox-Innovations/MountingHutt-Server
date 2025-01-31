

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=250)),
                ('image', models.ImageField(blank=True, null=True, upload_to='activities')),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blogs')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_time', models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=250)),
                ('image', models.ImageField(blank=True, null=True, upload_to='room')),
                ('capacity', models.PositiveIntegerField()),
                ('description', models.TextField(max_length=250)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='food')),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('category', models.CharField(blank=True, choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg'), ('Hot', 'Hot'), ('Cool', 'Cool')], max_length=20, null=True)),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('time', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foodtime', to='admins.item_category')),
            ],
        ),
    ]

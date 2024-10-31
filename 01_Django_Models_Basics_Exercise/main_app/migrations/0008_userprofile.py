# Generated by Django 5.0.4 on 2024-06-28 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_product_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=65, unique=True)),
                ('first_name', models.CharField(max_length=40, null=True)),
                ('last_name', models.CharField(max_length=40, null=True)),
                ('email', models.EmailField(default='students@softuni.bg', max_length=254, unique=True)),
                ('bio', models.TextField(max_length=120)),
                ('profile_image_url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
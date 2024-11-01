# Generated by Django 5.0.4 on 2024-06-27 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(null=True)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('duration_in_days', models.PositiveIntegerField(null=True, verbose_name='Duration in Days')),
                ('estimated_hours', models.FloatField(null=True, verbose_name='Estimated Hours')),
                ('start_date', models.DateField(auto_now_add=True, null=True, verbose_name='Start Date')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_edited_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

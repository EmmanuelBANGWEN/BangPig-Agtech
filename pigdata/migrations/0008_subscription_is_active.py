# Generated by Django 5.1.4 on 2025-02-15 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pigdata', '0007_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]

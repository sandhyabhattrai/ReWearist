# Generated by Django 5.1.7 on 2025-03-23 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wearist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='instock',
            field=models.BooleanField(default=True),
        ),
    ]

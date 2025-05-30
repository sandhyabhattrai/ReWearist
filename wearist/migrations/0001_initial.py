# Generated by Django 5.1.7 on 2025-03-23 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('category', models.CharField(max_length=100)),
                ('colour', models.CharField(max_length=50)),
                ('imageurl', models.CharField(max_length=300)),
                ('size', models.CharField(max_length=2)),
                ('material', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

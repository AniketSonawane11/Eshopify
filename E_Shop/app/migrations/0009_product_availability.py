# Generated by Django 5.1.6 on 2025-03-07 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_rename_nmae_brand_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Availability',
            field=models.CharField(choices=[('In Stock', 'In Stock'), ('Out Of Stock', 'Out Of Stock')], max_length=100, null=True),
        ),
    ]

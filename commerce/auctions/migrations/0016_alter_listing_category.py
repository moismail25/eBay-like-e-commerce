# Generated by Django 3.2.5 on 2021-08-01 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('fashion', 'Fashion'), ('others', 'Others'), ('electronics', 'Electronics'), ('toys', 'Toys')], max_length=64),
        ),
    ]
# Generated by Django 3.2.5 on 2021-07-25 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('toys', 'Toys'), ('electronics', 'Electronics'), ('others', 'Others'), ('fashion', 'Fashion')], max_length=64),
        ),
    ]

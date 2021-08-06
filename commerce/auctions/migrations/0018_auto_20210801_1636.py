# Generated by Django 3.2.5 on 2021-08-01 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20210801_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('electronics', 'Electronics'), ('others', 'Others'), ('fashion', 'Fashion'), ('toys', 'Toys')], max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, height_field=450, null=True, upload_to='images/', width_field=640),
        ),
    ]

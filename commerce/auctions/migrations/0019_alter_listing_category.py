# Generated by Django 3.2.5 on 2021-08-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20210801_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('electronics', 'Electronics'), ('fashion', 'Fashion'), ('toys', 'Toys'), ('others', 'Others')], max_length=64),
        ),
    ]

# Generated by Django 4.1.3 on 2022-12-13 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listings_watchlist_alter_bids_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='category',
            field=models.CharField(choices=[('Cars', 'Car'), ('Appliances', 'Appliances'), ('Sports', 'Sports')], default='Cars', max_length=64),
        ),
    ]

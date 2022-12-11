# Generated by Django 4.1.3 on 2022-12-10 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_listing_listings'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='watchlist',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='bids',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='listings',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

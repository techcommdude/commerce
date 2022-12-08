# Generated by Django 4.1.3 on 2022-12-08 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=300)),
                ('startingBid', models.FloatField(max_length=64)),
                ('url', models.CharField(blank=True, max_length=128)),
                ('category', models.CharField(choices=[('1', '1'), ('2', '2')], default=1, max_length=64)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='get_buyer_listings', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='get_creator_listings', to=settings.AUTH_USER_MODEL)),
                ('watchers', models.ManyToManyField(blank=True, related_name='get_watched_listings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=100)),
                ('createdDate', models.DateTimeField(auto_now=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_comments', to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_user_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currentBid', models.FloatField(blank=True, null=True)),
                ('bidAmount', models.FloatField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_auction_listings', to='auctions.listing')),
                ('user_bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_user_bids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

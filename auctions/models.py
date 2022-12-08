from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listings(models.Model):

    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="all_creator_listings")
    buyer = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name="all_buyer_listings")
    watchers = models.ManyToManyField(
        User, blank=True, related_name="all_watched_listings")
    createdDate = models.DateTimeField(default=timezone.now, auto_now=True)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    startingBid = models.FloatField(max_length=64)
    url = models.CharField(max_length=128, blank=True)
    Clothes = 'Clothes'
    Cars = 'Cars'
    Houses = 'Houses'
    Categories = [Clothes, 'Clothes', Cars, 'Cars', Houses, 'Houses']
    category = models.CharField(
        max_length=64, choices=Categories, default=Clothes)

    def __str__(self) -> str:
        return f"{self.title} - {self.startingBid}"


class Bids(models.Model):
    currentBid = models.FloatField(blank=True, null=True)
    offeringBid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.offeringBid}"


class Comments(models.Model):
    pass

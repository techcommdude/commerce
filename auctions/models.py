from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

Category_Choices = ((("Cars", "Cars"), ("Appliances", "Appliances"), ("Sports", "Sports")))


class Listing(models.Model):

    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="get_creator_listings", blank=False)
    buyer = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.PROTECT, related_name="get_buyer_listings")
    watchers = models.ManyToManyField(
        User, blank=True, related_name="get_watched_listings")
    # TODO: Not sure how to handle this date.
    createdDate = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    startingBid = models.FloatField(max_length=64)
    # blank = true means the field is not required.
    url = models.CharField(max_length=128, blank=True)
    category = models.CharField(
        max_length=64, choices=Category_Choices, default="Cars")

    def __str__(self) -> str:
        return f"Listing Title: {self.title} - Starting bid: {self.startingBid}"


class Bids(models.Model):
    auction = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="get_auction_listings")
    # must be at least as high as the starting bid.  Is there a point to this one?
    currentBid = models.FloatField(blank=True, null=True)
    # bid at which the offer was accepted and the listing is now closed and inactive.
    bidAmount = models.FloatField()
    # If a user is deleted, all bids associated with that user should also be deleted.
    user_bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_user_bids")
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"User that bid: {self.user_bidder} - Bid amount: {self.bidAmount}"


class Comments(models.Model):
    comment = models.CharField(max_length=100)
    # TODO: Not sure how to handle this date.
    createdDate = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_user_comments")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="get_comments")

    def __str__(self) -> str:
        return f"User: {self.user} - Comment: {self.comment} - Listing: {self.listing}"

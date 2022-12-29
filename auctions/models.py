from datetime import timezone
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):

    # The creator of the listing who can close it.
    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="get_creator_listings", blank=False)
    # Person who won the auction and bought it.  Cannot be the person who created it.
    buyer = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.PROTECT, related_name="get_buyer_listings")
    watchers = models.ManyToManyField(
        User, blank=True, related_name="get_watched_listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    # This is the starting price that the user who creates the listing specifies.
    startingBid = models.FloatField(max_length=64)
    createdDate = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    # blank = true means the field is not required.
    url = models.CharField(max_length=128, blank=True)
    category = models.CharField(
        max_length=45)

    def __str__(self) -> str:
        return f"Listing Title: {self.title} - Starting bid: {self.startingBid}"

class Bids(models.Model):
    auction = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="get_auction_listings")
    # This is the current bid on the item.  This item must be at least as high as previous that was bid or it is rejected.
    # Keep updating this amount and with the current highest price.  Keep the original price in the listing.
    currentBid = models.FloatField(blank=True, default=0.0)
    # The is the bid that the user submits on the form.
    bidAmount = models.FloatField(null=True, default=0.0)
    # If a user is deleted, all bids associated with that user should also be deleted.
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"User that bid: {self.user_bidder} - Bid amount: {self.bidAmount} - Current bid: {self.currentBid}"


class Comments(models.Model):
    comment = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_user_comments")
    listing = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="get_comments")

    def __str__(self) -> str:
        return f"User: {self.user} - Comment: {self.comment} - Listing: {self.listing}"

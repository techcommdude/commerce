from datetime import timezone
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Cars = 'Cars'
# Appliances = 'Appliances'
# Sports = 'Sports'
# NewCategory = 'NewCategory'
# Category_Choices = ((Cars, 'Car'), (Appliances, 'Appliances'), (Sports, 'Sports'), (NewCategory, 'Children\'s Stuff'))


class Listings(models.Model):

    creator = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="get_creator_listings", blank=False)
    buyer = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.PROTECT, related_name="get_buyer_listings")
    watchers = models.ManyToManyField(
        User, blank=True, related_name="get_watched_listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    # This is the starting price that the user who creates the listing specifies.
    startingBid = models.FloatField(max_length=64)
    # TODO: Does this work here?
    watchlist = models.CharField(blank=True, max_length=300)
    createdDate = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    # blank = true means the field is not required.
    url = models.CharField(max_length=128, blank=True)
    category = models.CharField(
        max_length=64)

    def __str__(self) -> str:
        return f"Listing Title: {self.title} - Starting bid: {self.startingBid}"


class Bids(models.Model):
    auction = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="get_auction_listings")
    # This is the current bid on the item.  This item must be at least as high as previous that was bid or it is rejected.
    # Keep updating this amount and with the current highest price, or else update the price in the listing.
    currentBid = models.FloatField(blank=True, default=0.0)
    # bid at which the offer was accepted and the listing is now closed and inactive.
    bidAmount = models.FloatField(null=True, default=0.0)
    # If a user is deleted, all bids associated with that user should also be deleted.
    user_bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_user_bids")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"User that bid: {self.user_bidder} - Bid amount: {self.bidAmount} - Current bid: {self.currentBid}"


class Comments(models.Model):
    comment = models.CharField(max_length=100)
    # TODO: Not sure how to handle this date.
    createdDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_user_comments")
    listing = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="get_comments")

    def __str__(self) -> str:
        return f"User: {self.user} - Comment: {self.comment} - Listing: {self.listing}"

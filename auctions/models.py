from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    bid = models.FloatField(default = 0)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bid")
    def __str__(self):
        return f"Bid of {self.bid} from {self.user}"

class AuctionListings(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name="auctionlistings", default = None)
    nameitem = models.CharField(max_length=32)
    description = models.CharField(max_length=100)
    bid = models.ForeignKey(Bid, on_delete = models.CASCADE, related_name = "auctionlistings", default = None)
    url = models.CharField(max_length=1000)
    category = models.CharField(max_length=32)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watch_listings")
    is_closed = models.BooleanField(default=False, blank=True, null=True)
    def __str__(self): 
        return f"{self.nameitem}: {self.bid}"

class Comments(models.Model):
    writer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
    listing = models.ForeignKey(AuctionListings, on_delete = models.CASCADE, related_name = "comments")
    text = models.CharField(max_length=100)

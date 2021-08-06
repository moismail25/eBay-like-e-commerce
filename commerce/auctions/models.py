from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from ckeditor.fields import RichTextField


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = {
        ("fashion", "Fashion"),
        ("electronics", "Electronics"),
        ("toys", "Toys"),
        ("others", "Others"),
    }

    title = models.CharField(max_length=64)
    description = RichTextField(blank=True, null=True)
    image = models.ImageField(default='default.png', blank=True, null=True, upload_to="images/")
    starting_bid = models.DecimalField(max_digits=1000, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    category = models.CharField(max_length=64, choices=CATEGORIES)
    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"Listing {self.pk}: {self.title}"

class Bid(models.Model):
    bid = models.DecimalField(max_digits=1000, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    listing = models.ForeignKey(Listing, on_delete=CASCADE)

    def __str__(self):
        return f"Bid {self.pk} by {self.user} on {self.listing}"

class Comment(models.Model):
    comment = models.TextField(max_length=6000)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    listing = models.ForeignKey(Listing, on_delete=CASCADE)
    def __str__(self):
        return f"Comment {self.pk} by {self.user} on {self.listing}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    listing = models.ForeignKey(Listing, on_delete=CASCADE)
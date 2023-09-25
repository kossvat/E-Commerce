from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    
    def __str__(self):
        return self.name
    

class Listing(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=150)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="all_creator_listings")
    # buyer = models.ForeignKey(User, on_delete=models.PROTECT)
    watchers = models.ManyToManyField(User, blank=True, related_name="watched_by")
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user} : {self.offer}'
    

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="get_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}: ({self.created_date})"

    
    
    
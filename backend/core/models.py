from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField()
    rating = models.FloatField()
    reviews_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating}★)"

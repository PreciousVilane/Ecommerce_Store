from django.db import models
from django.conf import settings
from store.models import Product

User = settings.AUTH_USER_MODEL

""" For users to leave reviews"""


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    verified = models.BooleanField(default=False)  # <-- New field

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product} ({'Verified' if self.verified else 'Unverified'})"

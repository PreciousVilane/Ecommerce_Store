from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

"""Vendors stores"""


class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    product_image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self):
        return self.name

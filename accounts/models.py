from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)

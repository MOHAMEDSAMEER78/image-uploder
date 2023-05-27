from django.db import models

from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


class User(models.Model):
    user_name = models.TextField(max_length=30)
    user_email = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=10)
    profile_image = models.CharField(max_length=300, null=True, blank=True)

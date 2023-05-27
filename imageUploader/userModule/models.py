from django.db import models

from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


class User(models.Model):
    user_name = models.TextField(
        validators=[
            MaxValueValidator(30),
            MinValueValidator(10),
        ]
    )
    user_email = models.CharField(max_length=100, validators=[

    ])
    user_phone = models.CharField(max_length=10,
                                  validators=[
                                      RegexValidator(
                                          regex='^\d{10}$', message='Please enter a valid 10-digit mobile number.')
                                  ]
                                  )
    profile_image = models.CharField(max_length=300, null=True, blank=True)

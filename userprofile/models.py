from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class User(AbstractUser):

    password = models.CharField(max_length=128, null=True, blank=True)

    email = models.EmailField(unique=True)
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
        ('owner', 'Business Owner'),
        ('admin', 'Admin'),
    ]
    name = models.CharField(max_length=25,default=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    address_province = models.CharField(max_length=100, blank=True, null=True)
    address_district = models.CharField(max_length=100, blank=True, null=True)
    address_municipality = models.CharField(max_length=100, blank=True, null=True)
    address_ward = models.CharField(max_length=10, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            base_username = self.email.split('@')[0]
            slug_candidate = slugify(base_username)
            unique_slug = slug_candidate
            counter = 1
            while User.objects.filter(username=unique_slug).exists():
                unique_slug = f"{slug_candidate}-{counter}"
                counter += 1
            self.username = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
from django.db import models
from django.utils.text import slugify

class User(models.Model):
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
        ('owner', 'Business Owner'),
        ('admin', 'Admin'),
    ]

    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    address_province = models.CharField(max_length=100, blank=True, null=True)
    address_district = models.CharField(max_length=100, blank=True, null=True)
    address_municipality = models.CharField(max_length=100, blank=True, null=True)
    address_ward = models.CharField(max_length=10, blank=True, null=True)

   
    username = models.SlugField(max_length=50, unique=True, blank=True)



    def save(self, *args, **kwargs):
        if not self.username:  
            base_username = self.email.split('@')[0]
            self.username = slugify(base_username)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
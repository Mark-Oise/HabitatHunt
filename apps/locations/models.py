from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    iso_code = models.CharField(max_length=2)  
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class Province(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2)  # e.g. 'ON' for Ontario
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.province.abbreviation}"


class CustomLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location_text = models.CharField(
        max_length=360,  
        help_text="Enter area name and postal code (e.g. Downtown Toronto, M5V 3A8)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.location_text} ({self.user.username})"


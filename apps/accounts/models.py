from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Realtor(models.Model):
    # User and Company Information
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    years_in_business = models.IntegerField()

    # License Information
    license_number = models.CharField(max_length=20)
    license_state = models.CharField(max_length=2)
    specialization = models.CharField(max_length=255)

    # Social and Profile
    social_media_links = models.JSONField(default=dict)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='images/')

    # Performance Metrics
    total_properties_sold = models.IntegerField()
    total_listings = models.IntegerField()
    rating = models.FloatField()

    # Status Fields
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name



   
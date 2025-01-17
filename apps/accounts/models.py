from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_realtor = models.BooleanField(default=False)
    is_agency = models.BooleanField(default=False)


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


class Agency(models.Model):
    # Basic Information
    name = models.CharField(max_length=255)
    headquarters_address = models.CharField(max_length=255)
    main_phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField()
    
    # Business Details
    founding_date = models.DateField()
    license_number = models.CharField(max_length=50)
    operating_states = models.JSONField(default=list)
    number_of_offices = models.IntegerField()
    
    # Team Information
    number_of_agents = models.IntegerField()
    realtors = models.ManyToManyField(Realtor, related_name='agencies')
    
    # Financial Information
    annual_sales_volume = models.DecimalField(max_digits=12, decimal_places=2)
    commission_structure = models.JSONField(default=dict)
    
    # Marketing and Branding
    logo = models.ImageField(upload_to='agency_logos/')
    brand_colors = models.JSONField(default=dict)
    social_media_presence = models.JSONField(default=dict)
    
    # Status and Verification
    is_verified = models.BooleanField(default=False)
    membership_status = models.CharField(max_length=50)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

from django.db import models
from django.conf import settings
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
    REGION_TYPES = [
        ('PROVINCE', 'Province'),
        ('STATE', 'State'),
        ('TERRITORY', 'Territory'),
        ('OTHER', 'Other'),
    ]
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(
        max_length=10,
        help_text="Official abbreviation (e.g., ON, CA, NY)"
    )
    region_type = models.CharField(
        max_length=10,
        choices=REGION_TYPES,
        default='PROVINCE'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['country', 'code']
        verbose_name_plural = "Provinces/States"

    def __str__(self):
        return f"{self.name}, {self.country.iso_code}"
    

class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.province.abbreviation}"


class CustomLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location_text = models.CharField(
        max_length=360,  
        help_text="Enter area name and postal code (e.g. Downtown Toronto, M5V 3A8)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.location_text} ({self.user.username})"


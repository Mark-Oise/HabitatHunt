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
        return f"{self.name}, {self.province.code}"


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


class LocationScrapeLog(models.Model):
    """
    Logs location-based filtering activity during lead generation
    """
    LOCATION_TYPE_CHOICES = [
        ('custom', 'Custom Location'),
        ('city', 'City'),
        ('province', 'Province/State'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    location_name = models.CharField(max_length=255)  # Store the actual location name
    
    # Metrics
    total_leads_before_filter = models.IntegerField(default=0)
    leads_matched = models.IntegerField(default=0)
    leads_filtered_out = models.IntegerField(default=0)
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Success'),
            ('failed', 'Failed'),
            ('no_data', 'No Location Data Available')
        ],
        default='success'
    )
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['location_type']),
        ]

    def __str__(self):
        return f"{self.location_name} ({self.get_location_type_display()}) - {self.leads_matched} matches"

    @property
    def filter_efficiency(self):
        """Calculate what percentage of leads matched the location filter"""
        if self.total_leads_before_filter == 0:
            return 0
        return (self.leads_matched / self.total_leads_before_filter) * 100


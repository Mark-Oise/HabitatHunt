from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from apps.hashtags.models import Hashtag
from apps.platforms.models import Platform
from apps.targets.models import Target

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
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    years_in_business = models.IntegerField(blank=True, null=True)

    # License Information
    license_number = models.CharField(max_length=20, blank=True, null=True)
    license_state = models.CharField(max_length=2, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)

    # Social and Profile
    social_media_links = models.JSONField(default=dict, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True)

    # Performance Metrics
    total_properties_sold = models.IntegerField(default=0)
    total_listings = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)

    # Status Fields
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name or f"Realtor - {self.user.email}"



class RealtorPreference(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    targets = models.ManyToManyField(Target, blank=True, related_name='preferences')
    platforms = models.ManyToManyField(Platform, blank=True, related_name='realtor_preferences')
    min_engagement_score = models.IntegerField(default=0)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='preferences')
    engagement_threshold = models.IntegerField(default=50)
    default_frequency = models.CharField(
        max_length=20, 
        choices=[('one-time', 'One-time request'), ('recurring', 'Recurring request')],
        default='one-time'
    )
    repeat_days = models.IntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 

    def __str__(self):
        return f"{self.user.name}'s Preferences"
    


class UserNotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email Notifications
    email_notifications_enabled = models.BooleanField(default=True, 
        help_text="Receive email notifications for important updates")
    new_leads_email = models.BooleanField(default=True,
        help_text="Get email notifications when new leads are generated")
    account_updates_email = models.BooleanField(default=True,
        help_text="Get email notifications about important account changes")
    marketing_emails = models.BooleanField(default=True,
        help_text="Receive promotional emails and special offers")

    # In-App Notifications
    in_app_notifications = models.BooleanField(default=True,
        help_text="Receive notifications within the HabitatHunt dashboard")
    
    class Meta:
        verbose_name = "User Notification Preference"
        verbose_name_plural = "User Notification Preferences"

    def __str__(self):
        return f"{self.user.email}'s Notification Preferences"
    
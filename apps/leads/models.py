from django.db import models
from django.conf import settings
from apps.platforms.models import Platform
from apps.targets.models import Target
from apps.hashtags.models import Hashtag
# Create your models here.


class RawComment(models.Model):
    username = models.CharField(max_length=255)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']



class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'), 
        ('in_progress', 'In Progress'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]

    CATEGORY_CHOICES = [
        ('cold', 'Cold'),
        ('warm', 'Warm'), 
        ('hot', 'Hot'),
    ]

    # User and basic info
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255) 
    message = models.TextField(blank=True)
    profile_url = models.URLField(blank=True, null=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    # Lead scoring
    sentiment_score = models.FloatField(default=0.0)
    engagement_score = models.FloatField(default=0.0)
    
    # Classification
    source = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True, related_name='leads')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='cold')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f'{self.name} - {self.category}'
    

    def get_direct_message_url(self):
        if self.source == 'instagram':
            return f'https://www.instagram.com/direct/new/?username={self.username}/'
        elif self.source == 'facebook':
            return f'https://m.me/{self.username}/'
        else:
            return None
        

    #     """
    #     Automatically categorize lead based on sentiment and engagement scores
    #     """
    #     if self.sentiment_score > 0.8 and self.engagement_score > 50:
    #         self.category = 'hot'
    #     elif self.sentiment_score > 0.5 and self.engagement_score > 20:
    #         self.category = 'warm'
    #     else:
    #         self.category = 'cold'
    #     self.save()

    # def save(self, *args, **kwargs):
    #     """
    #     Override save to ensure lead is categorized before saving
    #     """
    #     if not self.pk:  # Only categorize on creation
    #         self.categorize_lead()
    #     super().save(*args, **kwargs)

    def get_activity_timeline(self):
        """Get activity timeline ordered by most recent first"""
        return self.activity.all().order_by('-created_at')



class LeadPreference(models.Model):
    """
    Stores user's default preferences for lead generation.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lead_preferences')
    platforms = models.ManyToManyField(Platform, blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    targets = models.ManyToManyField(Target, blank=True)
    engagement_threshold = models.IntegerField(default=50)
    default_frequency = models.CharField(
        max_length=20, 
        choices=[('one-time', 'One-time request'), ('recurring', 'Recurring request')],
        default='one-time'
    )
    repeat_days = models.IntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lead Preference"
        verbose_name_plural = "Lead Preferences"

    def __str__(self):
        return f"{self.user.email}'s Lead Preferences"



class ActivityTimeline(models.Model):
    ACTION_CHOICES = [
        ('dm_sent', 'DM Sent'),
        ('dm_replied', 'DM Replied'),
        ('call_made', 'Call Made'),
        ('status_update', 'Status Update')
    ]
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activity')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.get_action_display()} for {self.lead} at {self.created_at}'
    


class Note(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.lead}'
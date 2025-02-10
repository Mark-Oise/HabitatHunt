from django.db import models
from django.conf import settings

# Create your models here.

PLATFORM_CHOICES = [
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
]

class RawComment(models.Model):
    username = models.CharField(max_length=255)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='other')
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
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)

    # Lead scoring
    sentiment_score = models.FloatField(default=0.0)
    engagement_score = models.FloatField(default=0.0)
    
    # Classification
    source = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='other')
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

    # def categorize_lead(self):
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
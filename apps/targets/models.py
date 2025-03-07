from django.db import models
from django.conf import settings
from apps.platforms.models import Platform


# Create your models here.
class Target(models.Model):
    """
    Stores social media profiles/pages that users want to monitor for leads.
    """
    username = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='targets')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    last_scraped = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Profile metadata
    follower_count = models.IntegerField(null=True, blank=True)
    following_count = models.IntegerField(null=True, blank=True)
    post_count = models.IntegerField(null=True, blank=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True)


    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['username']),
            models.Index(fields=['is_active']),
        ]
        unique_together = ['user', 'username']  # Prevent duplicate tracking

    def __str__(self):
        return f"{self.username} ({self.user.email})"
    


class TargetScrapeLog(models.Model):
    """
    Logs scraping activity for social media targets
    """
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name='scrape_logs')
    comments_scraped = models.IntegerField(default=0)
    leads_generated = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Success'),
            ('failed', 'Failed'),
            ('partial', 'Partial Success')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

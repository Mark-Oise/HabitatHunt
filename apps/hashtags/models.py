from django.db import models
from django.conf import settings
from apps.platforms.models import Platform


# Create your models here.
class Hashtag(models.Model):
    """
    Stores hashtags that users want to track.
    """
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hashtags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'user'] 

    def __str__(self):
        return self.name

class HashtagScrapeLog(models.Model):
    """
    Logs scraping activity for hashtag searches
    """
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='scrape_logs')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    posts_scraped = models.IntegerField(default=0)
    interactions_scraped = models.IntegerField(default=0)
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
    scrape_duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['hashtag', 'platform', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"#{self.hashtag.name} on {self.platform.display_name} - {self.get_status_display()}"
from django.db import models
from django.conf import settings


# Create your models here.

PLATFORM_CHOICES = [
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
]

class Hashtag(models.Model):
    """
    Stores hashtags that users want to track.
    """
    name = models.CharField(max_length=100, unique=True)
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hashtags')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from django.db import models
from django.conf import settings
from apps.platforms.models import Platform


# Create your models here.
class Hashtag(models.Model):
    """
    Stores hashtags that users want to track.
    """
    name = models.CharField(max_length=100, unique=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hashtags')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
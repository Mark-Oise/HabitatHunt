from django.db import models

# Create your models here.
class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    direct_message_url_template = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.display_name
    
    def get_direct_message_url(self, username):
        if self.direct_message_url_template:
            return self.direct_message_url_template.format(username=username)
        return None
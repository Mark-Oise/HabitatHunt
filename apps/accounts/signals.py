from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Realtor

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_realtor(sender, instance, created, **kwargs):
    if created:
        Realtor.objects.create(user=instance)

# Ensure the signal is connected
post_save.connect(create_realtor, sender=settings.AUTH_USER_MODEL)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User, Realtor, RealtorPreference

@receiver(post_save, sender=User)
def create_realtor_and_preferences(sender, instance, created, **kwargs):
    if created:
        Realtor.objects.create(user=instance)
        RealtorPreference.objects.create(user=instance)

# Ensure the signal is connected
post_save.connect(create_realtor_and_preferences, sender=User)
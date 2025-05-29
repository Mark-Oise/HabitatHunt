from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User, Realtor, RealtorPreference
from apps.leads.models import LeadPreference
from apps.platforms.models import Platform

@receiver(post_save, sender=User)
def create_realtor_and_preferences(sender, instance, created, **kwargs):
    if created:
        Realtor.objects.create(user=instance)
        RealtorPreference.objects.create(user=instance)
        
        # Create lead preference
        lead_preference = LeadPreference.objects.create(user=instance)
        
        # Set Facebook and Instagram as default platforms - fixed query
        default_platforms = Platform.objects.filter(
            name__in=['Facebook', 'Instagram']
        )
        
        if default_platforms.exists():
            lead_preference.platforms.add(*default_platforms)

# Ensure the signal is connected
post_save.connect(create_realtor_and_preferences, sender=User)
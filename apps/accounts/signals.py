from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User, Realtor, RealtorPreference
from apps.leads.models import LeadPreference
from apps.platforms.models import Platform
from apps.hashtags.models import Hashtag

@receiver(post_save, sender=User)
def create_realtor_and_preferences(sender, instance, created, **kwargs):
    if created:
        Realtor.objects.create(user=instance)
        RealtorPreference.objects.create(user=instance)
        
        # Create lead preference
        lead_preference = LeadPreference.objects.create(user=instance)
        
        # Set Facebook and Instagram as default platforms
        default_platforms = Platform.objects.filter(
            name__in=['Facebook', 'Instagram']
        )
        
        if default_platforms.exists():
            lead_preference.platforms.add(*default_platforms)
            
            # Default real estate hashtags
            default_hashtags = [
                "realestate", "realtor", "realestateagent", "realtorlife", 
                "realty", "property", "househunting", "homesweethome", 
                "dreamhome", "forsale"
            ]
            
            # Create hashtags for this user and add to lead preferences
            created_hashtags = []
            for tag_name in default_hashtags:
                hashtag, created = Hashtag.objects.get_or_create(
                    name=tag_name,
                    user=instance
                )
                created_hashtags.append(hashtag)
            
            # Add all hashtags to lead preferences
            if created_hashtags:
                lead_preference.hashtags.add(*created_hashtags)

# Ensure the signal is connected
post_save.connect(create_realtor_and_preferences, sender=User)
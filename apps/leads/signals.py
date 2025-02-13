from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead, ActivityTimeline

@receiver(post_save, sender=Lead)
def create_lead_activity(sender, instance, created, **kwargs):
    """
    Signal to create an ActivityTimeline entry when a new Lead is created
    """
    if created:
        ActivityTimeline.objects.create(
            lead=instance,
            user=instance.user,
            action='status_update',
            description='Lead created'
        )

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .services import LeadGenerationService
from .models import LeadPreference
from apps.targets.models import TargetScrapeLog
from apps.hashtags.models import HashtagScrapeLog
from apps.locations.models import LocationScrapeLog
from apps.platforms.models import Platform
from apps.targets.models import Target
from apps.hashtags.models import Hashtag
from apps.locations.models import CustomLocation, City, Province
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_lead_generation_request(self, task_data, user_id):
    """
    Background task for processing lead generation requests
    """
    try:
        user = User.objects.get(id=user_id)
        service = LeadGenerationService()
        
        # Update task status
        self.update_state(
            state='PROGRESS',
            meta={'status': 'Starting lead generation...', 'progress': 10}
        )
        
        # Convert IDs back to objects
        form_data = deserialize_task_data(task_data)
        
        self.update_state(
            state='PROGRESS',
            meta={'status': 'Processing targets and hashtags...', 'progress': 30}
        )
        
        # Process the request
        result = service.process_lead_request(form_data, user)
        
        self.update_state(
            state='PROGRESS',
            meta={'status': 'Saving leads...', 'progress': 80}
        )
        
        # Handle recurring requests
        if task_data['frequency'] == 'recurring':
            save_or_update_recurring_preference(task_data, user)
        
        logger.info(f"Lead generation completed for user {user.id}: {result}")
        
        self.update_state(
            state='SUCCESS',
            meta={
                'status': 'Lead generation completed!',
                'progress': 100,
                'results': result
            }
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Lead generation failed for user {user_id}: {str(e)}")
        
        self.update_state(
            state='FAILURE',
            meta={'status': f'Error: {str(e)}', 'progress': 0}
        )
        raise

def deserialize_task_data(task_data):
    """
    Convert serialized IDs back to Django objects
    """
    return {
        'platforms': Platform.objects.filter(id__in=task_data['platforms']),
        'targets': Target.objects.filter(id__in=task_data['targets']),
        'hashtags': Hashtag.objects.filter(id__in=task_data['hashtags']),
        'custom_locations': CustomLocation.objects.filter(id__in=task_data['custom_locations']),
        'cities': City.objects.filter(id__in=task_data['cities']),
        'provinces': Province.objects.filter(id__in=task_data['provinces']),
        'engagement_threshold': task_data['engagement_threshold'],
        'frequency': task_data['frequency'],
        'repeat_days': task_data['repeat_days'],
    }

def save_or_update_recurring_preference(task_data, user):
    """
    Save or update user's recurring lead generation preferences
    """
    try:
        # Get or create lead preference
        preference, created = LeadPreference.objects.get_or_create(
            user=user,
            defaults={
                'engagement_threshold': task_data['engagement_threshold'],
                'default_frequency': 'recurring',
                'repeat_days': task_data['repeat_days']
            }
        )
        
        if not created:
            # Update existing preference
            preference.engagement_threshold = task_data['engagement_threshold']
            preference.default_frequency = 'recurring'
            preference.repeat_days = task_data['repeat_days']
            preference.save()
        
        # Update many-to-many relationships
        preference.platforms.set(Platform.objects.filter(id__in=task_data['platforms']))
        preference.targets.set(Target.objects.filter(id__in=task_data['targets']))
        preference.hashtags.set(Hashtag.objects.filter(id__in=task_data['hashtags']))
        preference.custom_locations.set(CustomLocation.objects.filter(id__in=task_data['custom_locations']))
        preference.cities.set(City.objects.filter(id__in=task_data['cities']))
        preference.provinces.set(Province.objects.filter(id__in=task_data['provinces']))
        
        logger.info(f"Saved recurring preferences for user {user.id}")
        
    except Exception as e:
        logger.error(f"Error saving recurring preferences for user {user.id}: {e}")

@shared_task
def process_recurring_requests():
    """
    Process all recurring lead generation requests that are due
    """
    # Get all users with recurring preferences
    recurring_prefs = LeadPreference.objects.filter(
        default_frequency='recurring'
    )
    
    for pref in recurring_prefs:
        # Check if it's time to run (based on repeat_days)
        last_run = pref.updated_at
        next_run = last_run + timedelta(days=pref.repeat_days)
        
        if timezone.now() >= next_run:
            # Prepare form data from preferences
            form_data = {
                'platforms': list(pref.platforms.all()),
                'targets': list(pref.targets.all()),
                'hashtags': list(pref.hashtags.all()),
                'custom_locations': list(pref.custom_locations.all()),
                'cities': list(pref.cities.all()),
                'provinces': list(pref.provinces.all()),
                'engagement_threshold': pref.engagement_threshold,
            }
            
            # Queue the lead generation task
            process_lead_generation_request.delay(form_data, pref.user.id)
            
            # Update the preference timestamp
            pref.updated_at = timezone.now()
            pref.save()

@shared_task
def cleanup_old_scrape_logs():
    """
    Clean up old scrape logs from all sources (older than 30 days)
    """
    cutoff_date = timezone.now() - timedelta(days=30)
    
    # Clean up target logs
    target_deleted = TargetScrapeLog.objects.filter(
        created_at__lt=cutoff_date
    ).delete()[0]
    
    # Clean up hashtag logs
    hashtag_deleted = HashtagScrapeLog.objects.filter(
        created_at__lt=cutoff_date
    ).delete()[0]
    
    # Clean up location logs
    location_deleted = LocationScrapeLog.objects.filter(
        created_at__lt=cutoff_date
    ).delete()[0]
    
    total_deleted = target_deleted + hashtag_deleted + location_deleted
    
    logger.info(f"Cleaned up {total_deleted} old scrape logs (Targets: {target_deleted}, Hashtags: {hashtag_deleted}, Locations: {location_deleted})")
    return f"Cleaned up {total_deleted} old scrape logs"

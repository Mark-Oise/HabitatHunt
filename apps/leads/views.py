from django.shortcuts import render
from .models import Lead
from apps.platforms.models import Platform
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from .forms import UpdateLeadForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RequestLeadForm
from apps.targets.models import Target
from apps.hashtags.models import Hashtag
from apps.locations.models import CustomLocation, City, Province
from django.contrib import messages
from .tasks import process_lead_generation_request




def get_lead_context(user):
    """Helper function to get common lead form context"""
    # Get user preferences
    preferences = user.lead_preferences
    
    # Get all available data with efficient queries
    all_custom_locations = CustomLocation.objects.filter(user=user)
    all_cities = City.objects.all().select_related('province')
    all_provinces = Province.objects.all()
    
    return {
        'preferences': preferences,
        'platforms': Platform.objects.filter(is_active=True),
        'hashtags': Hashtag.objects.filter(user=user),
        'targets': Target.objects.filter(user=user),
        'custom_locations': all_custom_locations,
        'cities': all_cities,
        'provinces': all_provinces,
        'custom_locations_count': preferences.custom_locations.count(),
        'cities_count': preferences.cities.count(),
        'provinces_count': preferences.provinces.count(),
    }



def get_paginated_leads(request):
    # Query leads with ordering
    leads = Lead.objects.filter(user=request.user).prefetch_related('activity').order_by('-created_at')
    
    # Handle pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(leads, 10)  # Show 10 leads per page
    
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


# Create your views here.


def leads(request):
    if request.method == 'POST':
        # Check if this is a lead request form submission
        if 'request_lead_form' in request.POST:
            form = RequestLeadForm(request.user, request.POST)
            if form.is_valid():
                # Process the form data and queue the task
                success = process_lead_request(form.cleaned_data, request.user)
                
                if success:
                    messages.success(
                        request, 
                        'Lead generation request submitted successfully! You will be notified when it completes.'
                    )
                else:
                    messages.error(
                        request,
                        'There was an error submitting your lead generation request. Please try again.'
                    )
            else:
                # Add this to debug form errors
                messages.error(request, f'Form validation failed: {form.errors}')
            
            return redirect('leads:leads')
        else:
            # Handle lead update form
            lead = get_object_or_404(Lead, id=request.POST.get('lead_id'), user=request.user)
            form = UpdateLeadForm(request.POST, instance=lead)
            if form.is_valid():
                form.save()
                # Get updated leads with proper ordering
                leads = get_paginated_leads(request)
                
                # Return the entire table contents
                return render(request, 'leads/components/lead_items.html', {
                    'leads': leads,
                    'platforms': Platform.objects.filter(is_active=True),
                    'status_choices': Lead.STATUS_CHOICES,
                })
    
    # Get lead data
    leads = get_paginated_leads(request)
    total_leads = Lead.objects.filter(user=request.user).count()

    context = get_lead_context(request.user)
    
    
    
    context.update({
        'leads': leads,
        'total_leads': total_leads,
        'status_choices': Lead.STATUS_CHOICES,
        'request_lead_form': RequestLeadForm(request.user),
    })
        
    return render(request, 'leads/leads.html', context)


@require_http_methods(["POST"])
def bulk_delete_leads(request):
    delete_all = request.GET.get('delete_all') == 'true'
    
    if delete_all:
        # Delete all leads for the current user
        Lead.objects.filter(user=request.user).delete()
    else:
        # Delete selected leads
        selected_leads = request.POST.getlist('selected_leads')
        Lead.objects.filter(
            id__in=selected_leads,
            user=request.user
        ).delete()
    
    # Get updated leads with pagination
    leads = get_paginated_leads(request)
    total_leads = Lead.objects.filter(user=request.user).count()
        
    return render(request, 'leads/components/lead_container.html', {
        'leads': leads,
        'total_leads': total_leads,
        'platforms': Platform.objects.filter(is_active=True),
        'status_choices': Lead.STATUS_CHOICES,
    })


def delete_lead(request, lead_id):
    if request.method == 'POST':
        lead = get_object_or_404(Lead, id=lead_id, user=request.user)
        lead.delete()
        
        # Get updated leads with pagination
        leads = get_paginated_leads(request)
        total_leads = Lead.objects.filter(user=request.user).count()
        
        # Return the entire container with updated counts
        return render(request, 'leads/components/lead_container.html', {
            'leads': leads,
            'total_leads': total_leads,
            'platforms': Platform.objects.filter(is_active=True),
            'status_choices': Lead.STATUS_CHOICES,
        })


@login_required
def get_lead_preferences(request):
    try:
        context = get_lead_context(request.user)
        return render(request, 'leads/components/form_preference_fields.html', context)
    except AttributeError:
        return HttpResponse(status=400)
    

def process_lead_request(form_data, user):
    """
    Process the lead generation request by queuing a Celery task
    """
    try:
        # Prepare the form data for the task
        # Convert QuerySets to lists of IDs for serialization
        task_data = {
            'platforms': [p.id for p in form_data['platforms']],
            'targets': [t.id for t in form_data['targets']],
            'hashtags': [h.id for h in form_data['hashtags']],
            'custom_locations': [cl.id for cl in form_data['custom_locations']],
            'cities': [c.id for c in form_data['cities']],
            'provinces': [p.id for p in form_data['provinces']],
            'engagement_threshold': form_data['engagement_threshold'],
            'frequency': form_data['frequency'],
            'repeat_days': form_data.get('repeat_days', 7),
        }
        
        # Queue the task
        task = process_lead_generation_request.delay(task_data, user.id)
        
        # Optional: Track the task status
        # TaskStatus.objects.create(
        #     user=user,
        #     task_id=task.id,
        #     task_type='lead_generation',
        #     status='pending'
        # )
        
        return True
        
    except Exception as e:
        print(f"Error queuing lead generation task: {e}")
        return False

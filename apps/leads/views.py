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
                # Process the form data
                # In a real implementation, you would pass this to a task queue
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
    
    # Create request lead form
    request_lead_form = RequestLeadForm(request.user)
    
    context = {
        'leads': leads,
        'total_leads': total_leads,
        'platforms': Platform.objects.filter(is_active=True),
        'status_choices': Lead.STATUS_CHOICES,
        'request_lead_form': request_lead_form,
        'targets': Target.objects.filter(user=request.user),
        'hashtags': Hashtag.objects.filter(user=request.user),
    }
        
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

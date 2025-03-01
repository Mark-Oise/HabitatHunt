from django.shortcuts import render
from .models import Lead, PLATFORM_CHOICES
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from .forms import AddLeadForm, UpdateLeadForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


# Create your views here.


def leads(request):
    if request.method == 'POST':
        lead = get_object_or_404(Lead, id=request.POST.get('lead_id'), user=request.user)
        form = UpdateLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            # Get updated leads with proper ordering
            leads = Lead.objects.filter(user=request.user).prefetch_related('activity').order_by('-created_at')
            
            # Return the entire table contents
            return render(request, 'leads/components/lead_items.html', {
                'leads': leads,
                'platform_choices': PLATFORM_CHOICES,
                'status_choices': Lead.STATUS_CHOICES,
            })
        
    
    leads = Lead.objects.filter(user=request.user).prefetch_related('activity')
    total_leads = leads.count()
    
    # Handle pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(leads, 10)  # Show 10 leads per page
    
    try:
        leads = paginator.page(page)
    except PageNotAnInteger:
        leads = paginator.page(1)
    except EmptyPage:
        leads = paginator.page(paginator.num_pages)
        
    context = {
        'leads': leads,
        'total_leads': total_leads,
        'platform_choices': PLATFORM_CHOICES,
        'status_choices': Lead.STATUS_CHOICES,  # Make sure this matches the model's attribute name
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
    
    # Get updated leads with proper ordering
    leads = Lead.objects.filter(user=request.user).prefetch_related('activity').order_by('-created_at')
    total_leads = leads.count()
    
    # Handle pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(leads, 10)
    
    try:
        leads = paginator.page(page)
    except PageNotAnInteger:
        leads = paginator.page(1)
    except EmptyPage:
        leads = paginator.page(paginator.num_pages)
        
    context = {
        'leads': leads,
        'total_leads': total_leads,
        'platform_choices': PLATFORM_CHOICES,
        'status_choices': Lead.STATUS_CHOICES,
    }
    
    return render(request, 'leads/components/lead_container.html', context)


def delete_lead(request, lead_id):
    if request.method == 'POST':
        lead = get_object_or_404(Lead, id=lead_id, user=request.user)
        lead.delete()
        
        # Get updated leads with proper ordering
        leads = Lead.objects.filter(user=request.user).prefetch_related('activity').order_by('-created_at')
        total_leads = leads.count()
        
        # Handle pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(leads, 10)  # Show 10 leads per page
        
        try:
            leads = paginator.page(page)
        except PageNotAnInteger:
            leads = paginator.page(1)
        except EmptyPage:
            leads = paginator.page(paginator.num_pages)
        
        # Return the entire container with updated counts
        return render(request, 'leads/components/lead_container.html', {
            'leads': leads,
            'total_leads': total_leads,
            'platform_choices': PLATFORM_CHOICES,
            'status_choices': Lead.STATUS_CHOICES,
        })



    if request.method == "DELETE":
        selected_leads = request.POST.getlist('selected_leads')
        
        # Delete only leads that belong to the current user
        Lead.objects.filter(
            id__in=selected_leads,
            user=request.user
        ).delete()
        
        # Get updated leads with proper ordering
        leads = Lead.objects.filter(user=request.user).prefetch_related('activity').order_by('-created_at')
        total_leads = leads.count()
        
        # Handle pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(leads, 10)
        
        try:
            leads = paginator.page(page)
        except PageNotAnInteger:
            leads = paginator.page(1)
        except EmptyPage:
            leads = paginator.page(paginator.num_pages)
            
        context = {
            'leads': leads,
            'total_leads': total_leads,
            'platform_choices': PLATFORM_CHOICES,
            'status_choices': Lead.STATUS_CHOICES,
        }
        
        return render(request, 'dashboard/components/leads/lead_container.html', context)

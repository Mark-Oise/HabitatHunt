from .models import Lead, Note
from apps.platforms.models import Platform
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
from django.http import HttpResponse
from datetime import datetime
from .forms import AddNoteForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def search_leads(request):
    search_query = request.GET.get('search', '').strip()
    leads = Lead.objects.filter(user=request.user)

    if search_query:
        leads = leads.filter(
            Q(name__icontains=search_query) |
            Q(username__icontains=search_query) 
            # Q(email__icontains=search_query)
        )

    return render(request, 'leads/components/lead_items.html', {
        'leads': leads,
        'search_query': search_query
    })



def filter_leads(request):
    leads = Lead.objects.filter(user=request.user)
    
    # Handle source filtering
    sources = request.GET.getlist('source')
    if sources:
        leads = leads.filter(source__id__in=sources)
    
    # Handle category filtering
    categories = request.GET.getlist('category')
    if categories:
        leads = leads.filter(category__in=categories)
    
    # Handle status filtering
    statuses = request.GET.getlist('status')
    if statuses:
        leads = leads.filter(status__in=statuses)
    
    # Handle sentiment score range
    sentiment_min = request.GET.get('sentiment_min')
    sentiment_max = request.GET.get('sentiment_max')
    if sentiment_min:
        leads = leads.filter(sentiment_score__gte=float(sentiment_min))
    if sentiment_max:
        leads = leads.filter(sentiment_score__lte=float(sentiment_max))
    
    # Handle engagement score range
    engagement_min = request.GET.get('engagement_min')
    engagement_max = request.GET.get('engagement_max')
    if engagement_min:
        leads = leads.filter(engagement_score__gte=float(engagement_min))
    if engagement_max:
        leads = leads.filter(engagement_score__lte=float(engagement_max))
    
    # Handle pagination
    paginator = Paginator(leads, 10)
    page = request.GET.get('page', 1)
    try:
        leads = paginator.page(page)
    except PageNotAnInteger:
        leads = paginator.page(1)
    except EmptyPage:
        leads = paginator.page(paginator.num_pages)
    
    context = {
        'leads': leads,
        'platforms': Platform.objects.filter(is_active=True),  # Add platforms to context
        'category_choices': Lead.CATEGORY_CHOICES,
        'status_choices': Lead.STATUS_CHOICES,
    }
    
    return render(request, 'leads/components/lead_items.html', context)


def export_leads_csv(request):
    # Get leads for current user
    leads = Lead.objects.filter(user=request.user)
    
    # Create the HttpResponse object with CSV header
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="HabitatHunt_leads_export_{timestamp}.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow([
        'Name', 'Username', 'Source', 'Category', 'Status',
        'Sentiment Score', 'Engagement Score', 'Created At'
    ])
    
    # Write data rows
    for lead in leads:
        writer.writerow([
            lead.name,
            lead.username,
            lead.get_source_display(),
            lead.get_category_display(),
            lead.get_status_display(),
            lead.sentiment_score,
            lead.engagement_score,
            lead.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response



def add_note(request, lead_id):
    if request.method == 'POST':
        form = AddNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.lead = Lead.objects.get(id=lead_id)
            note.author = request.user
            note.save()
            # Return just the new note template
            return render(request, 'leads/components/note_item.html', {'note': note})
    return HttpResponse(status=400)



@login_required
def delete_note(request, note_id):
    if request.method == 'DELETE':
        note = get_object_or_404(Note, id=note_id, lead__user=request.user)
        note.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=400)
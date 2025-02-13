from .models import Lead, PLATFORM_CHOICES
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search_leads(request):
    search_query = request.GET.get('search', '').strip()
    leads = Lead.objects.filter(user=request.user)

    if search_query:
        leads = leads.filter(
            Q(name__icontains=search_query) |
            Q(username__icontains=search_query) 
            # Q(email__icontains=search_query)
        )

    return render(request, 'dashboard/components/leads/lead_items.html', {
        'leads': leads,
        'search_query': search_query
    })



def filter_leads(request):
    leads = Lead.objects.filter(user=request.user)
    
    # Handle source filtering
    sources = request.GET.getlist('source')
    if sources:
        leads = leads.filter(source__in=sources)
    
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
        'platform_choices': PLATFORM_CHOICES,
        'category_choices': Lead.CATEGORY_CHOICES,
        'status_choices': Lead.STATUS_CHOICES,
    }
    
    return render(request, 'dashboard/components/leads/lead_items.html', context)
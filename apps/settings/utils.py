from django.db.models import Q
from apps.hashtags.models import Hashtag
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.platforms.models import Platform
from apps.targets.models import Target
from apps.leads.models import LeadPreference


def search_hashtags(request):
    search_query = request.GET.get('search', '').strip()
    hashtags = Hashtag.objects.filter(user=request.user)

    if search_query:
        hashtags = hashtags.filter(
            Q(name__icontains=search_query)
        )

    return render(request, 'settings/partials/hashtag_items.html', {
        'hashtags': hashtags,
        'search_query': search_query
    })


def search_targets(request):
    search_query = request.GET.get('search', '').strip()
    targets = Target.objects.filter(user=request.user)

    if search_query:
        targets = targets.filter(
            Q(username__icontains=search_query) |
            Q(platform__name__icontains=search_query) 
        )

    return render(request, 'settings/partials/target_items.html', {
        'targets': targets,
        'search_query': search_query
    })

def select_all_hashtags(request):
    """Select all hashtags for the current user in the lead preference form."""
    hashtags = Hashtag.objects.filter(user=request.user)
    lead_preference = LeadPreference.objects.get(user=request.user)
    
    # Mark all hashtags as selected in the context
    return render(request, 'settings/partials/hashtag_items.html', {
        'hashtags': hashtags,
        'lead_preference': lead_preference,
        'all_selected': True  # This will be used to check all boxes
    })

def clear_all_hashtags(request):
    """Clear all hashtag selections for the current user in the lead preference form."""
    hashtags = Hashtag.objects.filter(user=request.user)
    lead_preference = LeadPreference.objects.get(user=request.user)
    
    return render(request, 'settings/partials/hashtag_items.html', {
        'hashtags': hashtags,
        'lead_preference': lead_preference,
        'none_selected': True  # This will be used to uncheck all boxes
    })
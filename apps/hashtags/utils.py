from django.db.models import Q
from .models import Hashtag
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.platforms.models import Platform



def search_hashtags(request):
    search_query = request.GET.get('search', '').strip()
    hashtags = Hashtag.objects.filter(user=request.user)

    if search_query:
        hashtags = hashtags.filter(
            Q(name__icontains=search_query) |
            Q(platform__name__icontains=search_query) 
        )

    return render(request, 'hashtags/components/hashtag_items.html', {
        'hashtags': hashtags,
        'search_query': search_query
    })



def filter_hashtags(request):
    hashtags = Hashtag.objects.filter(user=request.user)
    
    # Track active filters
    active_filters = False
    
    # Handle platform filtering
    platforms = request.GET.getlist('platform')
    if platforms:
        hashtags = hashtags.filter(platform__id__in=platforms)
        active_filters = True
    
    # Handle pagination
    paginator = Paginator(hashtags, 10)
    page = request.GET.get('page', 1)
    try:
        hashtags = paginator.page(page)
    except PageNotAnInteger:
        hashtags = paginator.page(1)
    except EmptyPage:
        hashtags = paginator.page(paginator.num_pages)
    
    context = {
        'hashtags': hashtags,
        'platforms': Platform.objects.filter(is_active=True),  # Add platforms to context
        'active_filters': active_filters,
    }
    
    return render(request, 'hashtags/components/hashtag_items.html', context)




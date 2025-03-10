from django.db.models import Q
from .models import Target
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Target
from apps.platforms.models import Platform



def search_targets(request):
    search_query = request.GET.get('search', '').strip()
    targets = Target.objects.filter(user=request.user)

    if search_query:
        targets = targets.filter(
            Q(username__icontains=search_query)
        )

    return render(request, 'targets/components/target_items.html', {
        'targets': targets,
        'search_query': search_query
    })


def filter_targets(request):
    targets = Target.objects.filter(user=request.user)
    
    # Track active filters
    active_filters = False
    
    # Handle platform filtering
    platforms = request.GET.getlist('platform')
    if platforms:
        targets = targets.filter(platform__id__in=platforms)
        active_filters = True
    
    # Handle pagination
    paginator = Paginator(targets, 10)
    page = request.GET.get('page', 1)
    try:
        targets = paginator.page(page)
    except PageNotAnInteger:
        targets = paginator.page(1)
    except EmptyPage:
        targets = paginator.page(paginator.num_pages)
    
    context = {
        'targets': targets,
        'platforms': Platform.objects.filter(is_active=True),  # Add platforms to context
        'active_filters': active_filters,
    }
    
    return render(request, 'targets/components/target_items.html', context)




from django.db.models import Q
from apps.hashtags.models import Hashtag
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.platforms.models import Platform
from apps.targets.models import Target


def search_hashtags(request):
    search_query = request.GET.get('search', '').strip()
    hashtags = Hashtag.objects.filter(user=request.user)

    if search_query:
        hashtags = hashtags.filter(
            Q(name__icontains=search_query) |
            Q(platform__name__icontains=search_query) 
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
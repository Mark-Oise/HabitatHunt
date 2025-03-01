from django.db.models import Q
from .models import Hashtag
from django.shortcuts import render




def search_hashtags(request):
    search_query = request.GET.get('search', '').strip()
    hashtags = Hashtag.objects.filter(user=request.user)

    if search_query:
        hashtags = hashtags.filter(
            Q(name__icontains=search_query) |
            Q(platform__icontains=search_query) 
        )

    return render(request, 'hashtags/components/hashtag_items.html', {
        'hashtags': hashtags,
        'search_query': search_query
    })
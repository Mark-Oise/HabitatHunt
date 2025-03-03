from django.shortcuts import render
from .forms import HashtagForm
from .models import Hashtag
from apps.platforms.models import Platform
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404


# Helper function to get paginated hashtags
def get_paginated_hashtags(request):
    # Query hashtags with ordering
    hashtags = Hashtag.objects.filter(user=request.user).order_by('-created_at')
    
    # Handle pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(hashtags, 10)  # Show 10 hashtags per page
    
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


# Create your views here.
def hashtags(request): 
    if request.method == 'POST':
        form = HashtagForm(request.POST)
        if form.is_valid():
            hashtag = form.save(commit=False)
            hashtag.user = request.user
            hashtag.save()
            # Get updated hashtags after adding new one
            paginated_hashtags = get_paginated_hashtags(request)

        return render(request, 'hashtags/components/hashtag_items.html', {
                'hashtags': paginated_hashtags,
                'form': form, 
                'platforms': Platform.objects.filter(is_active=True)})

    form = HashtagForm()
    paginated_hashtags = get_paginated_hashtags(request)

    context = {
        'hashtags': paginated_hashtags,
        'form': form,
        'platforms': Platform.objects.filter(is_active=True),
    }

    return render(request, 'hashtags/hashtags.html', context)


def delete_hashtag(request, hashtag_id):
    if request.method == 'POST':
        hashtag = get_object_or_404(Hashtag, id=hashtag_id, user=request.user)
        hashtag.delete()
        
        # Get updated hashtags list with pagination
        paginated_hashtags = get_paginated_hashtags(request)
            
        return render(request, 'hashtags/components/hashtag_items.html', {
            'hashtags': paginated_hashtags,
        })

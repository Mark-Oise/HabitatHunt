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


    total_hashtags = Hashtag.objects.filter(user=request.user).count()
    form = HashtagForm()
    paginated_hashtags = get_paginated_hashtags(request)

    context = {
        'hashtags': paginated_hashtags,
        'total_hashtags': total_hashtags,
        'form': form,
        'platforms': Platform.objects.filter(is_active=True),
    }

    return render(request, 'hashtags/hashtags.html', context)





def bulk_delete_hashtags(request):
    delete_all = request.GET.get('delete_all') == 'true'
    
    if delete_all:
        # Delete all targets for the current user
        Hashtag.objects.filter(user=request.user).delete()
    else:
        # Delete selected targets
        selected_hashtags = request.POST.getlist('selected_hashtags')
        Hashtag.objects.filter(
            id__in=selected_hashtags,
            user=request.user
        ).delete()

    hashtags = Hashtag.objects.filter(user=request.user).order_by('-created_at')

    # Get updated hashtags list with pagination
    paginated_hashtags = get_paginated_hashtags(request)

    return render(request, 'hashtags/components/hashtag_items.html', {
            'hashtags': paginated_hashtags,
        })




def delete_hashtag(request, hashtag_id):
    if request.method == 'POST':
        hashtags = get_object_or_404(Hashtag, id=hashtag_id, user=request.user)
        hashtags.delete()
        
        # Get updated hashtags list with pagination
        paginated_hashtags = get_paginated_hashtags(request)
            
        return render(request, 'hashtags/components/hashtag_items.html', {
            'hashtags': paginated_hashtags,
        })

from django.shortcuts import render
from .forms import HashtagForm
from .models import Hashtag
from .models import PLATFORM_CHOICES
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404


# Create your views here.
def hashtags(request): 
    # Query hashtags with ordering
    hashtags = Hashtag.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = HashtagForm(request.POST)
        if form.is_valid():
            hashtag = form.save(commit=False)
            hashtag.user = request.user
            hashtag.save()
            # Refresh the queryset after adding new hashtag
            hashtags = Hashtag.objects.filter(user=request.user).order_by('-created_at')

        return render(request, 'hashtags/components/hashtag_items.html', {
                'hashtags': hashtags,
                'form': form, 
                'platform_choices': PLATFORM_CHOICES,})

    form = HashtagForm()
    # Handle pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(hashtags, 10)  # Show 10 hashtags per page
    
    try:
        hashtags = paginator.page(page)
    except PageNotAnInteger:
        hashtags = paginator.page(1)
    except EmptyPage:
        hashtags = paginator.page(paginator.num_pages)

    context = {
        'hashtags': hashtags,
        'form': form,
        'platform_choices': PLATFORM_CHOICES,
    }

    return render(request, 'hashtags/hashtags.html', context)




def delete_hashtag(request, hashtag_id):
    if request.method == 'POST':
        hashtag = get_object_or_404(Hashtag, id=hashtag_id, user=request.user)
        hashtag.delete()
        
        # Get updated hashtags list with ordering
        hashtags = Hashtag.objects.filter(user=request.user).order_by('-created_at')
        
        # Handle pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(hashtags, 10)  # Show 10 hashtags per page
        
        try:
            hashtags = paginator.page(page)
        except PageNotAnInteger:
            hashtags = paginator.page(1)
        except EmptyPage:
            hashtags = paginator.page(paginator.num_pages)
            
        return render(request, 'hashtags/components/hashtag_items.html', {
            'hashtags': hashtags,
        })

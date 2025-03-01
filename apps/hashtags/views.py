from django.shortcuts import render
from .forms import HashtagForm
from .models import Hashtag

# Create your views here.
def hashtags(request):
    # Initialize form variable outside the POST condition
    form = HashtagForm()
    
    if request.method == 'POST':
        form = HashtagForm(request.POST)
        if form.is_valid():
            form.save()

    hashtags = Hashtag.objects.filter(user=request.user)

    context = {
        'hashtags': hashtags,
        'form': form,
    }

    return render(request, 'hashtags/hashtags.html', context)

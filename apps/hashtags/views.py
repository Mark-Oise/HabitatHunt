from django.shortcuts import render
from .forms import HashtagForm
from .models import Hashtag

# Create your views here.
def hashtags(request):
    if request.method == 'POST':
        form = HashtagForm()
        if form.is_valid():
            form.save()

    hashtags = Hashtag.objects.filter(user=request.user)

    context = {
        'hashtags': hashtags,
        'form': form,
    }


    return render(request, 'hashtags/hashtags.html', context)

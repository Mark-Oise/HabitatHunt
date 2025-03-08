from django.db.models import Q
from .models import Target
from django.shortcuts import render



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
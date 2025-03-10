from django.shortcuts import render
from .forms import TargetForm
from .models import Target
from apps.platforms.models import Platform
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
# Create your views here.



# Helper function to get paginated hashtags
def get_paginated_targets(request):
    # Query targets with ordering
    targets = Target.objects.filter(user=request.user).order_by('-created_at')
    
    # Handle pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(targets, 10)  # Show 10 hashtags per page
    
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


# Create your views here.
def targets(request): 
    if request.method == 'POST':
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.save(commit=False)
            target.user = request.user
            target.save()
            # Get updated targets after adding new one
            paginated_targets = get_paginated_targets(request)

        return render(request, 'targets/components/target_items.html', {
                'targets': paginated_targets,
                'form': form, 
                'platforms': Platform.objects.filter(is_active=True)})
    

    total_targets = Target.objects.filter(user=request.user).count()

    form = TargetForm()
    paginated_targets = get_paginated_targets(request)

    context = {
        'targets': paginated_targets,
        'form': form,
        'platforms': Platform.objects.filter(is_active=True),
        'total_targets': total_targets
    }

    return render(request, 'targets/targets.html', context)




def bulk_delete_targets(request):
    delete_all = request.GET.get('delete_all') == 'true'
    
    if delete_all:
        # Delete all targets for the current user
        Target.objects.filter(user=request.user).delete()
    else:
        # Delete selected targets
        selected_targets = request.POST.getlist('selected_targets')
        Target.objects.filter(
            id__in=selected_targets,
            user=request.user
        ).delete()

    targets = Target.objects.filter(user=request.user).order_by('-created_at')

    # Get updated hashtags list with pagination
    paginated_targets = get_paginated_targets(request)

    return render(request, 'targets/components/target_items.html', {
            'targets': paginated_targets,
        })




def delete_target(request, target_id):
    if request.method == 'POST':
        target = get_object_or_404(Target, id=target_id, user=request.user)
        target.delete()
        
        # Get updated hashtags list with pagination
        paginated_targets = get_paginated_targets(request)
            
        return render(request, 'targets/components/target_items.html', {
            'targets': paginated_targets,
        })

from django.shortcuts import render
from .models import Lead, PLATFORM_CHOICES
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect

# Create your views here.


def leads(request):
    leads = Lead.objects.filter(user=request.user)
    total_leads = leads.count()
    
    # Handle pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(leads, 10)  # Show 10 leads per page
    
    try:
        leads = paginator.page(page)
    except PageNotAnInteger:
        leads = paginator.page(1)
    except EmptyPage:
        leads = paginator.page(paginator.num_pages)
        
    context = {
        'leads': leads,
        'total_leads': total_leads,
        'platform_choices': PLATFORM_CHOICES,  # Add platform choices to context
    }
        
    return render(request, 'dashboard/leads.html', context)


# def create_lead(request):
#     if request.method == 'POST':
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             lead = form.save(commit=False)
#             lead.user = request.user
#             lead.save()
#             return redirect('leads')
#     else:
#         form = LeadForm()
#     return render(request, 'leads/create_lead.html', {'form': form})


# def update_lead(request, lead_id):
#     lead = Lead.objects.get(id=lead_id)
#     if request.method == 'POST':
#         form = LeadForm(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect('leads')
#     else:
#         form = LeadForm(instance=lead)
#     return render(request, 'leads/update_lead.html', {'form': form})


# def delete_lead(request, lead_id):
#     lead = Lead.objects.get(id=lead_id)
#     lead.delete()
#     return redirect('leads')

from django.shortcuts import render
from .models import Lead, PLATFORM_CHOICES
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from .forms import AddLeadForm, UpdateLeadForm


# Create your views here.


def leads(request):
    if request.method == 'POST':
        form = UpdateLeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.user = request.user
            lead.save()
            return redirect('leads:leads')
        
    else:
        form = UpdateLeadForm()

    leads = Lead.objects.filter(user=request.user).prefetch_related('activity')
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
        'platform_choices': PLATFORM_CHOICES,
        'status_choices': Lead.STATUS_CHOICES,  # Make sure this matches the model's attribute name
    }
        
    return render(request, 'dashboard/leads.html', context)




# def delete_lead(request, lead_id):
#     lead = Lead.objects.get(id=lead_id)
#     lead.delete()
#     return redirect('leads')

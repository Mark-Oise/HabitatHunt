from .models import Lead
from django.db.models import Q
from django.shortcuts import render


def search_leads(request):
    search_query = request.GET.get('search', '').strip()
    leads = Lead.objects.filter(user=request.user)

    if search_query:
        leads = leads.filter(
            Q(name__icontains=search_query) |
            Q(username__icontains=search_query) 
            # Q(email__icontains=search_query)
        )

    return render(request, 'dashboard/components/leads/lead_items.html', {
        'leads': leads,
        'search_query': search_query
    })
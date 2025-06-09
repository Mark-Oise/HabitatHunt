from django.shortcuts import render
from django.db.models import Q
from .models import CustomLocation, Province


def search_custom_locations(request):
    search_query = request.GET.get('search', '').strip()
    custom_locations = CustomLocation.objects.filter(user=request.user)

    if search_query:
        custom_locations = custom_locations.filter(
            Q(location_text__icontains=search_query) 
        )

    return render(request, 'locations/partials/custom_location_items.html', {
        'custom_locations': custom_locations,
        'search_query': search_query
    })


def search_provinces(request):
    search_query = request.GET.get('search', '').strip()
    provinces = Province.objects.all()

    if search_query:
        provinces = provinces.filter(
            Q(name__icontains=search_query)
        )
    
    return render(request,  'locations/partials/province_items.html', {
        'provinces': provinces,
        'search_query': search_query
    })
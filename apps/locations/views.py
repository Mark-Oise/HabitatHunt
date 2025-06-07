from django.shortcuts import render
from .models import Province  # Add this import

# Create your views here.
def locations(request):
    provinces = Province.objects.all().select_related('country')  # Get all provinces with country data
    return render(request, 'locations/locations.html', {'provinces': provinces})
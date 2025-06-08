from django.shortcuts import render
from .models import Province  # Add this import

# Create your views here.
def locations(request):
    provinces = Province.objects.all().select_related('country')  # Get all provinces with country data
    return render(request, 'locations/locations.html', {'provinces': provinces})



def add_custom_location(request):
    pass

def delete_custom_location(request, location_id):
    pass

def update_custom_location(request, location_id):
    pass


def search_custom_location(request, location_id):
    pass





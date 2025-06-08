from django.shortcuts import render
from .models import Province, CustomLocation  # Add this import
from .forms import CustomLocationForm
from django.shortcuts import redirect

# Create your views here.
def locations(request):
    provinces = Province.objects.all().select_related('country')  # Get all provinces with country data
    custom_locations = CustomLocation.objects.filter(user=request.user)
    custom_locations_count = custom_locations.count()
    context = {
        'provinces': provinces,
        'custom_locations': custom_locations,
        'custom_locations_count': custom_locations_count
    }
    return render(request, 'locations/locations.html', context)



def add_custom_location(request):
    if request.method == 'POST':
        form = CustomLocationForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            custom_locations = CustomLocation.objects.filter(user=request.user)
            return render(request, 'locations/partials/custom_location_elements.html', {
                'custom_locations': custom_locations,
                'custom_locations_count': custom_locations.count()
            })
    else:
        form = CustomLocationForm(user=request.user)
    return render(request, 'locations/add_custom_location.html', {'form': form})



def delete_custom_location(request, location_id):
    location = CustomLocation.objects.get(id=location_id)
    location.delete()
    return render(request, 'locations/partials/custom_location_elements.html', {
        'custom_locations': CustomLocation.objects.filter(user=request.user),
        'custom_locations_count': CustomLocation.objects.filter(user=request.user).count()
    })


def update_custom_location(request, location_id):
    pass


def search_custom_location(request, location_id):
    pass





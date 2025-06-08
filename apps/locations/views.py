from django.shortcuts import render
from .models import Province  # Add this import
from .forms import CustomLocationForm
from django.shortcuts import redirect

# Create your views here.
def locations(request):
    provinces = Province.objects.all().select_related('country')  # Get all provinces with country data
    return render(request, 'locations/locations.html', {'provinces': provinces})



def add_custom_location(request):
    if request.method == 'POST':
        form = CustomLocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('locations')
    else:
        form = CustomLocationForm()
    return render(request, 'locations/add_custom_location.html', {'form': form})



def delete_custom_location(request, location_id):
    pass

def update_custom_location(request, location_id):
    pass


def search_custom_location(request, location_id):
    pass





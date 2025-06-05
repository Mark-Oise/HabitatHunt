from django.shortcuts import render

# Create your views here.
def locations(request):
    return render(request, 'locations/locations.html')
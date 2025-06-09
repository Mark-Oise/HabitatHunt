from django.urls import path
from . import views, utils

app_name = 'locations'

urlpatterns = [
    path('', views.locations, name='locations'),
    path('add-custom-location/', views.add_custom_location, name='add_custom_location'),
    path('delete-custom-location/<int:location_id>/', views.delete_custom_location, name='delete_custom_location'),
    path('search-custom-locations/', utils.search_custom_locations, name='search_custom_locations'),
    path('search-provinces', utils.search_provinces, name='search_provinces'),
]

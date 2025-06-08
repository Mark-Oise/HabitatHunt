from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('', views.locations, name='locations'),
    path('add-custom-location/', views.add_custom_location, name='add_custom_location'),
    path('delete-custom-location/<int:location_id>/', views.delete_custom_location, name='delete_custom_location'),
]

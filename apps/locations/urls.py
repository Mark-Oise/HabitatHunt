from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('', views.locations, name='locations'),
    path('add-custom-location/', views.add_custom_location, name='add_custom_location'),
]

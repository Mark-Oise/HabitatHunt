from django.urls import path
from . import views, utils

app_name = 'leads'

urlpatterns = [
    path('', views.leads, name='leads'),
    path('search/', utils.search_leads, name='search_leads'),
    path('filter/', utils.filter_leads, name='filter_leads'),
]
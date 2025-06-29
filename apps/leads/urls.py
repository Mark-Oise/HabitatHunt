from django.urls import path
from . import views, utils

app_name = 'leads'

urlpatterns = [
    
    path('', views.leads, name='leads'),
    path('search/', utils.search_leads, name='search_leads'),
    path('filter/', utils.filter_leads, name='filter_leads'),
    path('export-csv/', utils.export_leads_csv, name='export_csv'),

    # #Leads CRUD
    # path('add/', views.create_lead, name='add_lead'),
    # path('update/<int:lead_id>/', views.update_lead, name='update_lead'),
    path('delete/<int:lead_id>/', views.delete_lead, name='delete_lead'),
    path('bulk-delete/', views.bulk_delete_leads, name='bulk_delete_leads'),




    # Notes
    path('leads/<int:lead_id>/notes/add/', utils.add_note, name='add_note'),
    path('notes/<int:note_id>/delete/', utils.delete_note, name='delete_note'),

    path('preferences/', views.get_lead_preferences, name='get_lead_preferences'),

]
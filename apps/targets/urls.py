from django.urls import path
from . import views, utils

app_name = 'targets'

urlpatterns = [
    path('', views.targets, name='targets'),
    path('search/', utils.search_targets, name='search_targets'),
    path('delete/<int:target_id>/', views.delete_target, name='delete_target'),
    path('filter/', utils.filter_targets, name='filter_targets'),
]

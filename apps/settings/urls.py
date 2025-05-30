from django.urls import path
from . import views, utils

app_name = 'settings'


urlpatterns = [
    path('', views.settings, name='settings'),
    path('search-hashtags/', utils.search_hashtags, name='search_hashtags'),
    path('search-targets/', utils.search_targets, name='search_targets'),
    path('select-all-hashtags/', utils.select_all_hashtags, name='select_all_hashtags'),
    path('clear-all-hashtags/', utils.clear_all_hashtags, name='clear_all_hashtags'),
]
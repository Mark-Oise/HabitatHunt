from django.urls import path
from . import views, utils

app_name = 'hashtags'

urlpatterns = [
    path('', views.hashtags, name='hashtags'),
    path('search/', utils.search_hashtags, name='search_hashtags'),
]

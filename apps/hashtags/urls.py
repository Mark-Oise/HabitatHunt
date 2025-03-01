from django.urls import path
from . import views

app_name = 'hashtags'

urlpatterns = [
    path('', views.hashtags, name='hashtags'),
]

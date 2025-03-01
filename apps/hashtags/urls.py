from django.urls import path
from . import views

app_name = 'hashtags'

urlpatterns = [
    path('hashtags/', views.hashtags, name='hashtags'),
]

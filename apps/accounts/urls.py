from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('validate-password/', views.validate_password, name='validate_password'),
    path('validate-email/', views.validate_email, name='validate_email'),
]

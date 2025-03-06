from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from .validators import CustomPasswordValidator
import json
from django.core.exceptions import ValidationError
from .models import User
from django.views.decorators.http import require_POST
# Create your views here.

@require_POST
def validate_password(request):
    """Real-time password validation with template response"""
    password = request.POST.get('password1', '')
    validator = CustomPasswordValidator()
    
    try:
        validator.validate(password)
        context = {
            'password_valid': True,
            'requirements_met': True
        }
    except ValidationError as e:
        context = {
            'password_valid': False,
            'password_errors': e.messages
        }
    
    return render(request, 'account/components/alerts.html', context)



@require_POST
def validate_email(request):
    """Real-time email validation with template response"""
    email = request.POST.get('email', '')
    exists = User.objects.filter(email=email).exists()
    
    return render(request, 'account/components/email_feedback.html', {
        'email_exists': exists,
        'email': email
    })

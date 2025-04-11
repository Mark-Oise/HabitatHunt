from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RealtorSettingsForm, CustomChangePasswordForm
from apps.accounts.models import Realtor
from django.contrib.auth import update_session_auth_hash




# Create your views here.

def settings(request):
    realtor_settings = Realtor.objects.get(user=request.user)
    realtor_settings_form = RealtorSettingsForm(instance=realtor_settings)
    password_change_form = CustomChangePasswordForm(user=request.user)

    if request.method == 'POST':
        if 'realtor_settings_form' in request.POST:
            realtor_settings_form = RealtorSettingsForm(request.POST, instance=realtor_settings)
            if realtor_settings_form.is_valid():
                realtor_settings_form.save()  # This will now save both Realtor and User models
                messages.success(request, 'Personal information updated successfully.')
                return redirect('settings:settings')
            else:
                messages.error(request, 'Please correct the errors below.')
        
        elif 'password_change_form' in request.POST:
            password_change_form = CustomChangePasswordForm(request.user, request.POST)
            if password_change_form.is_valid():
                password_change_form.save()

                # Update session to prevent logging out after password change
                update_session_auth_hash(request, request.user)
                
                messages.success(request, 'Password updated successfully.')
                return redirect('settings:settings')
            else:
                messages.error(request, 'Please correct the errors below.')

    context = {
        'realtor_settings_form': realtor_settings_form,
        'password_change_form': password_change_form,
        'realtor': realtor_settings,
        'user': request.user,
    }
    return render(request, 'settings/settings.html', context)
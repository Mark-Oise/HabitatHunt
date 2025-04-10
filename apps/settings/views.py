from django.shortcuts import render




# Create your views here.

def settings(request):
    # realtor_settings_form = RealtorSettingsForm(instance=request.user.realtor)
    
    # if request.method == 'POST':
    #     realtor_settings_form = RealtorSettingsForm(request.POST, instance=request.user.realtor)
    #     if realtor_settings_form.is_valid():
    #         realtor_settings_form.save()
    #         messages.success(request, 'Personal information updated successfully.')
    #         return redirect('settings:settings')
    #     messages.error(request, 'Please correct the errors below.')

    # context = {
    #     'realtor_settings_form': realtor_settings_form,
        
    # }
    return render(request, 'settings/settings.html', context)
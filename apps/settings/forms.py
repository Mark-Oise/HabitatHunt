from django import forms
from apps.accounts.models import Realtor, User, UserNotificationPreference
from allauth.account.forms import ChangePasswordForm

class RealtorSettingsForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Realtor
        fields = [
            'company_name',
            'company_address',
            'phone',
            'years_in_business',
            'license_number',
            'license_state',
            'specialization'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['name'].initial = self.instance.user.name

    def save(self, commit=True):
        realtor = super().save(commit=False)
        if commit:
            # Save the realtor instance
            realtor.save()
            # Update the associated user's name
            realtor.user.name = self.cleaned_data['name']
            realtor.user.save()
        return realtor
    

class UserNotificationSettings(forms.ModelForm):
    class Meta:
        model = UserNotificationPreference
        fields = [
            'email_notifications_enabled',
            'new_leads_email',
            'account_updates_email',
            'marketing_emails',
            'in_app_notifications',
        ]



class CustomChangePasswordForm(ChangePasswordForm):
    oldpassword = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput()
    )
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput()
    )
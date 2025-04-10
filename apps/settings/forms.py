from django import forms
from apps.accounts.models import Realtor


class RealtorSettingsForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True)
    company_name = forms.CharField(max_length=255, required=True)
    company_address = forms.CharField(max_length=255, required=True)
    phone = forms.CharField(max_length=20, required=True)
    years_in_business = forms.IntegerField(required=True)
    license_number = forms.CharField(max_length=20, required=True)
    license_state = forms.CharField(max_length=2, required=True)
    specialization = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Realtor
        fields = [
            'name',
            'company_name',
            'company_address',
            'phone',
            'years_in_business',
            'license_number',
            'license_state',
            'specialization'
        ]

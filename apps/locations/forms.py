from django import forms
from .models import CustomLocation

class CustomLocationForm(forms.ModelForm):
    class Meta:
        model = CustomLocation
        fields = ['location_text']


        
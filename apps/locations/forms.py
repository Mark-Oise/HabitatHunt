from django import forms
from .models import CustomLocation

class CustomLocationForm(forms.ModelForm):
    class Meta:
        model = CustomLocation
        fields = ['location_text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


        
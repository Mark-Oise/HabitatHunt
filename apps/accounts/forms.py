from allauth.account.forms import SignupForm
from django import forms
from .models import RealtorPreference


class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=256, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.save()
        return user
    

class RealtorPreferenceForm(forms.ModelForm):
    class Meta:
        model = RealtorPreference
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['hashtags'].queryset = self.fields['hashtags'].queryset.filter(user=self.instance.user)

from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=256, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.save()
        return user
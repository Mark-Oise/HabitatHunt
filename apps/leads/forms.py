from django import forms
from .models import Note, Lead
from apps.platforms.models import Platform
from apps.targets.models import Target
from apps.hashtags.models import Hashtag
from apps.leads.models import LeadPreference
from apps.locations.models import CustomLocation, City, Province


class RequestLeadForm(forms.Form):
    platforms = forms.ModelMultipleChoiceField(
        queryset=Platform.objects.filter(is_active=True),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'hidden'})
    )
    
    targets = forms.ModelMultipleChoiceField(
        queryset=Target.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'hidden'}),
        label="Pages"
    )
    
    hashtags = forms.ModelMultipleChoiceField(
        queryset=Hashtag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'hidden'})
    )
    
    engagement_threshold = forms.IntegerField(
        min_value=0,
        max_value=100,
        initial=50,
        required=True,
        widget=forms.NumberInput(attrs={'type': 'range'})
    )
    
    FREQUENCY_CHOICES = [
        ('one-time', 'One-time request'),
        ('recurring', 'Recurring request')
    ]
    
    frequency = forms.ChoiceField(
        choices=FREQUENCY_CHOICES,
        initial='one-time',
        widget=forms.RadioSelect
    )
    
    repeat_days = forms.IntegerField(
        min_value=1,
        max_value=30,
        initial=7,
        required=False,
        widget=forms.NumberInput(attrs={'min': '1', 'max': '30'})
    )
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filter targets and hashtags by user
            self.fields['targets'].queryset = Target.objects.filter(user=user)
            self.fields['hashtags'].queryset = Hashtag.objects.filter(user=user)



class UpdateLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'name', 'username', 'email', 'phone', 'location', 
            'message', 'engagement_score', 'sentiment_score', 
            'source', 'category', 'status'
        ]



class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note_text']



class LeadPreferenceForm(forms.ModelForm):
    """
    Form for setting default lead generation preferences.
    """
    class Meta:
        model = LeadPreference
        exclude = ['user', 'created_at', 'updated_at']
        
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filter related fields by user
            self.fields['hashtags'].queryset = Hashtag.objects.filter(user=user)
            self.fields['targets'].queryset = Target.objects.filter(user=user)

            # Add location filters
            self.fields['custom_locations'].queryset = CustomLocation.objects.filter(user=user)
            self.fields['cities'].queryset = City.objects.all()
            self.fields['provinces'].queryset = Province.objects.all()
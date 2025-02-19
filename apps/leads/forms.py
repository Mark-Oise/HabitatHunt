from django import forms
from .models import Note, Lead

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'username', 'profile_url', 'email', 'phone', 'location', 'message', 'engagement_score', 'sentiment_score', 'source',
                'category', 'status']
        

class UpdateLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'username', 'email', 'phone', 'location', 'message', 'engagement_score', 'sentiment_score', 'source',
                'category', 'status']


class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note_text']
from django import forms
from .models import Note

# class LeadForm(forms.ModelForm):
#     class Meta:
#         model = Lead
#         fields = ['name', 'email', 'phone', 'message', 'interest', 'confidence_score', 'source']


class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note_text']
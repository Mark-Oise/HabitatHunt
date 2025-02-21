from django import forms
from .models import Listing, ListingImage


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'price', 'property_type', 'location',
            'contact_info', 'open_house_date', 'status'
        ]

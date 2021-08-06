from django import forms
from .models import Listing

class NewListing(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('user', 'closed')
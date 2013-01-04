from django import forms
from django.contrib.auth.models import User

from models import Shirt, ShirtShot


class ShotForm(forms.ModelForm):
    class Meta:
        model = ShirtShot
        fields = ['image']

class ShirtForm(forms.ModelForm):
    def clean_created_by(self):
        return (self.cleaned_data['created_by'] or 'Unknown')

    def clean_introduced(self):
        return self.cleaned_data['introduced'] or 'Unknown'

    class Meta:
        model = Shirt
        fields = ['created_by', 'introduced', 'description', 'tags']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

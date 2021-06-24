from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from libri_im.models import NewUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length = 255, help_text="Required. Add a valid email address.")
    class Meta:
        model = NewUser
        fields = ('email','username','password1','password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = NewUser.objects.get(email=email)
        except Exception:
            return email
        raise forms.ValidationError(f'Email {user.email} is already in use.')
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = NewUser.objects.get(username=username)
        except Exception:
           return username
        raise forms.ValidationError(f'Email {user.username} is already in use.')

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

class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ('email', 'password')
    
    def clean(self):
        if self.is_valid:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid login. Check email and password again.")

    # def save(self):
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     user = aithenticate(email=email, password=password)
    #     if user:
    #         login(request, user)

    

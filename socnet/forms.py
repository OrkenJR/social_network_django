from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)

        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    birth_date = forms.DateField()

    class Meta:
        model = UserProfile
        fields = ['image', 'quote', 'birth_date']

        widgets = {'image': forms.FileInput(
            attrs={'style': 'display: none;', 'class': 'form-control', 'required': False}
        )}


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    error_messages = {
        'invalid_login': (
            "Invalid password or login"
        ),

    }

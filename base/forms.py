from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserProfile
from . import constant


class NewUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your Password', 'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Repeat your password', 'class': 'form-control'}),
        }

    def clean(self):
        return super(NewUserForm, self).clean()


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role']


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from . import constant


class NewUserForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=constant.USER_TYPE)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'profile_picture','first_name', 'last_name', 'password1', 'password2', 'user_type' ]
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your Password', 'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Repeat your password', 'class': 'form-control'}),
        }

    def clean(self):
        return super(NewUserForm, self).clean()


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'profile_picture')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'email'}),
            'first_name': forms.EmailInput(attrs={'placeholder': 'first_name'}),
            'last_name': forms.EmailInput(attrs={'placeholder': 'last_name'}),
            'profile_image': forms.EmailInput(attrs={'placeholder': 'image'}),

        }

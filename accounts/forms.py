from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import AppUser


class AppUserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        }),
    )

    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
            }),
        }
        labels = {
            'username': 'Username',
        }
        help_texts = {
            'username': 'Choose a unique username.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password',
        })

        self.fields['password1'].help_text = 'Your password must meet the security requirements.'
        self.fields['password2'].help_text = 'Enter the same password again for verification.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AppUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username',
        }),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
        }),
    )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('email', 'profile_image', 'bio', 'city')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell something about yourself...',
                'rows': 4,
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city',
            }),
        }
        labels = {
            'email': 'Email',
            'profile_image': 'Profile Image',
            'bio': 'Bio',
            'city': 'City',
        }
        help_texts = {
            'bio': 'Optional field.',
            'city': 'Optional field.',
        }
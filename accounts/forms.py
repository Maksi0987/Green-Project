from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'birth_date', 'location', 'website']
        labels = {
            'avatar': 'Фото профілю',
            'bio': 'Про себе',
            'birth_date': 'Дата народження',
            'location': 'Місто',
            'website': 'Веб-сайт',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-input', 'style': 'padding: 8px;'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'website': forms.URLInput(attrs={'class': 'form-input'}),
        }
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import *


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Введите Ваш адрес электронной почты'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Введите Ваш пароль'})
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        labels = {
            'username': _('Электронная почта'),
            'password': _('Пароль')
        }

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Введите Ваш адрес электронной почты'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Введите Ваш пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Повторите Ваш пароль'})
    
    class Meta:
        model = CustomUser
        fields = ('email', )
        labels = {
            'email': _('Электронная почта')
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message', )
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Напишите свой комментарий...'})
        }
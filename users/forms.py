from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Don't forget "
            "that the password is case-sensitive."
        ),
    }

    username = forms.CharField(
        label=_('Username or email'),
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            link_text = _('request a new one')
            link = f'<a href="/resend-activation/">{link_text}</a>'
            msg = _(
                'Your account is not activated.\nPlease check your email for '
                'the activation link or {}.'
            )
            raise ValidationError(msg.format(link))


class RegistrationForm(UserCreationForm):
    username = forms.RegexField(
        label=_('Username'),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_('30 chars or fewer. Letters, digits and ' '@/./+/-/_'),
        error_messages={
            'invalid': _(
                'This value may contain only letters, numbers and '
                '@/./+/-/_ characters'
            )
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': 'true',
                'autofocus': 'autofocus',
                'placeholder': '',
            }
        ),
    )

    email = forms.EmailField(label=_('Email'))

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'required': 'true',
                'placeholder': '',
            }
        ),
    )
    password2 = forms.CharField(
        label=_('Password yet again'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'type': 'password',
                'required': True,
                'placeholder': '',
            }
        ),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('User with this email already exists.')
        return email


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label='', max_length=254)


class EmailForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'email',
                'autofocus': 'autofocus',
            }
        ),
    )

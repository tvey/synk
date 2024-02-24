from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.db.models import Q
from django.views.generic import TemplateView

from .models import User
from .forms import RegistrationForm, EmailForm, LoginForm


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{timestamp}{user.is_active}'


token_generator = TokenGenerator()


def send_activation_link(request, user, first=True):
    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    mail_subject = _('Activate your account')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    html_message = render_to_string(
        'users/registration_activation_email.html',
        {
            'user': user,
            'domain': current_site,
            'uidb64': uid,
            'token': token,
            'protocol': protocol,
            'first': first,
        },
    )
    plain_message = strip_tags(html_message)

    send_mail(
        mail_subject,
        plain_message,
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=html_message,
    )


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        if not User.objects.filter(
            email__iexact=email, is_active=True
        ).exists():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_activation_link(request, user)
            msg = _(
                'Welcome! Please check your email to complete registration.'
            )
            messages.info(request, _(msg))
            return redirect('login')

        elif User.objects.filter(email__iexact=email, is_active=False).exists():
            return render(request, 'users/registration_activation_error.html')

        return redirect(request.path_info)

    return render(request, 'users/auth.html', {'form': form})


def activate_account(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect('dashboard')

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        msg = _('Great! Now you can login and synk more links.')
        messages.info(request, msg)
        return redirect('login')
    else:
        return render(request, 'users/registration_activation_error.html')


def resend_activation(request):
    if request.user.is_authenticated:
        messages.info(request, _('Your account is already activated.'))
        return redirect('dashboard')

    form = EmailForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email', None)
        try:
            user = User.objects.get(email__iexact=email)
            if user.is_active:
                messages.info(request, _('Your account is already activated.'))
                return redirect('login')
            send_activation_link(request, user, first=False)
            messages.info(
                request, _('Please check your email for the activation link.')
            )
            return redirect('login')
        except User.DoesNotExist:
            msg = _('Please entered the address you registered with.')
            messages.error(request, msg)
            return redirect(request.path_info)
    context = {'form': form}
    return render(request, 'users/registration_activation_resend.html', context)


class LoginUserView(LoginView):
    template_name = 'users/auth.html'
    redirect_authenticated_user = True
    form_class = LoginForm


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    old = request.POST.get('old_password')
    new = request.POST.get('new_password1')

    if form.is_valid():
        old = request.POST.get('old_password')
        new = request.POST.get('new_password1')
        if old == new:
            messages.info(request, _('You haven’t changed your password.'))
        else:
            user = form.save()
            update_session_auth_hash(request, user)
            messages.info(request, _('Your password was successfully updated!'))
        return redirect('dashboard')

    return render(request, 'users/password_change.html', {'form': form})


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_settings.html'

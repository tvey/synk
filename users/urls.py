from django.urls import path
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .views import (
    register,
    activate_account,
    resend_activation,
    change_password,
    LoginUserView,
)
from .forms import LoginForm, ResetPasswordForm

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate-account'),
    path('resend-activation/', resend_activation, name='resend-activation'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('change-password/', change_password, name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        "reset-password/",
        PasswordResetView.as_view(
            template_name="users/password_reset.html",
            form_class=ResetPasswordForm,
            html_email_template_name="users/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset-password-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

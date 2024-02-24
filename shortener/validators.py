import re

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, RegexValidator


def validate_url(value):
    validator = URLValidator()

    if not value.startswith('http'):
        value = 'http://' + value
    try:
        validator(value)
    except:
        raise ValidationError(
            'Please make sure to use a good link :)', code='invalid'
        )
    return value


def validate_domain(value):
    '''Prevent using *this site* as a source link.'''
    current_site = Site.objects.get_current()
    domain = current_site.domain
    pattern = r'(https?://)?{site}'
    match = re.match(pattern.format(site=domain), value)
    if match:
        raise ValidationError('This one is already synked :)', code='invalid')
    return value


validate_code = RegexValidator(
    re.compile(r'^[-a-zA-Z0-9_]+\Z'),
    'Try to use only letters (a-z, A-Z), numbers, underscores and hyphens.',
    'invalid',
)


def validate_length(value):
    '''Handle length restrictions for the short link code.'''
    if len(value) < 4:
        msg = "That's a bit too short, start with 4 symbols."
        raise ValidationError(msg, code='invalid')
    elif len(value) > 30:
        msg = (
            "That's a bit too long, try to use at most 30 symbols. "
            f"That was {len(value)}."
        )
        raise ValidationError(msg, code='invalid')
    return value


def validate_forbidden(value):
    forbidden = [
        'login',
        'register',
        'activate',
        'resend-activation',
        'change-password',
        'reset-password',
        'password-reset-complete',
        'logout',
        'about',
        'join',
        'result',
        'edit',
        'create',
        'new',
        'yay',
        'dashboard',
        'admin',
        'sadmin',
        'api',
        'one',
        'synk',
    ]

    if value.lower() in forbidden:
        raise ValidationError("Sorry, but it's mine :)", code='invalid')
    return value

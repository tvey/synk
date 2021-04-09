from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone

from .validators import (
    validate_domain,
    validate_code,
    validate_length,
    validate_forbidden,
)
from .utils import generate_code


class Link(models.Model):
    source = models.TextField(validators=[URLValidator(), validate_domain])
    code = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_code, validate_length, validate_forbidden],
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.code:
            while True:
                code = generate_code(5)
                if not Link.objects.filter(code=code).exists():
                    break
            self.code = code
        self.updated = timezone.now()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Link({self.code})'

    def get_absolute_url(self):
        return self.code


class Click(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Click for {self.link}'

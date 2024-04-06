from django import template
from ..utils import decode_link

register = template.Library()


@register.filter
def decode_url(value):
    return decode_link(value)

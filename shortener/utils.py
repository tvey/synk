import secrets
import string
import urllib.parse

import idna
from idna.core import IDNAError, InvalidCodepoint

RANDOM_STRING_CHARS = (
    string.digits + string.ascii_uppercase + string.ascii_lowercase
)


def generate_shortcode(length=7, allowed_chars=RANDOM_STRING_CHARS):
    return ''.join(secrets.choice(allowed_chars) for _ in range(length))


def decode_link(value):
    """Decode a URL-encoded link string for display."""
    try:
        if '%' not in value and 'xn--' not in value:
            return value

        domain = urllib.parse.urlsplit(value).netloc

        if domain:
            decoded_domain = idna.decode(domain)
            url = value.replace(domain, decoded_domain)
            return urllib.parse.unquote(url)
    except (UnicodeError, IDNAError, InvalidCodepoint) as e:
        print(f'Error decoding URL: {e}')  # add logs
    except Exception as e:
        print(f'Unexpected error: {e}')  # add logs

    return urllib.parse.unquote(value)

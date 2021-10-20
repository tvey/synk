import secrets
import string

RANDOM_STRING_CHARS = (
    string.digits + string.ascii_uppercase + string.ascii_lowercase
)


def generate_shortcode(length=7, allowed_chars=RANDOM_STRING_CHARS):
    return ''.join(secrets.choice(allowed_chars) for _ in range(length))

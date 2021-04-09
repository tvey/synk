import secrets
import string

RANDOM_STRING_CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase


def generate_code(length=5, allowed_chars=RANDOM_STRING_CHARS):
    return ''.join(secrets.choice(allowed_chars) for i in range(length))


def check_exists(url):
    pass

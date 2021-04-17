import dotenv

from .base import *

dotenv.load_dotenv(BASE_DIR / '.env')

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

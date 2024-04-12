import requests
from celery import shared_task


@shared_task
def check_url_for_redirect(url):
    try:
        r = requests.head(url, allow_redirects=True)
        return r.status_code < 300 and r.url == url
    except requests.RequestException:
        return False

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    LinkCreateAPIView,
    LinkListAPIView,
    LinkDetailAPIView,
    LinkUpdateAPIView,
    LinkDeleteAPIView,
    AboutAPIView,
)

app_name = 'link-api'

urlpatterns = [
    path('', AboutAPIView.as_view(), name='about'),
    path('list/', LinkListAPIView.as_view(), name='list'),
    path('new/', LinkCreateAPIView.as_view(), name='create'),
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('update/<code>/', LinkUpdateAPIView.as_view(), name='update'),
    path('delete/<code>/', LinkDeleteAPIView.as_view(), name='delete'),
    path('<code>/', LinkDetailAPIView.as_view(), name='detail'),
]

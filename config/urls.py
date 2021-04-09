from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('users.urls')),
    path('sadmin/', admin.site.urls),
    path('api/', include('shortener.api.urls')),
    path('', include('shortener.urls')),
]

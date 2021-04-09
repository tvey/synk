from django.urls import path

from .views import (
    HomeView,
    ResultView,
    LinkRedirectView,
    LinkCreateView,
    LinkUpdateView,
    LinkDeleteView,
    DashboardView,
    SearchView,
    AboutView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('yay/', ResultView.as_view(), name='result'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('about/', AboutView.as_view(), name='about'),
    path('search/', SearchView.as_view(), name='search'),
    path('new/', LinkCreateView.as_view(), name='create'),
    path('edit/<slug:code>/', LinkUpdateView.as_view(), name='update'),
    path('delete/<slug:code>/', LinkDeleteView.as_view(), name='delete'),
    path('<slug:code>/', LinkRedirectView.as_view(), name='redirect'),
]

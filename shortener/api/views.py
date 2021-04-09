from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from shortener.models import Link
from .serializers import LinkCreateSerializer, LinkSerializer, LinkListSerializer


class LinkCreateAPIView(CreateAPIView):
    serializer_class = LinkCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = LinkCreateSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            instance = serializer.save(owner=self.request.user)
            protocol = 'https' if request.is_secure() else 'http'
            link = f'{protocol}://{request.get_host()}/{instance.code}/'
            data = {'link': link, 'code': instance.code}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LinkListAPIView(ListAPIView):
    serializer_class = LinkListSerializer

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = Link.objects.filter(owner=user).order_by('-updated')
        return queryset


class LinkDetailAPIView(RetrieveAPIView):
    serializer_class = LinkSerializer
    lookup_field = 'code'
    lookup_url_kwarg = 'code'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = Link.objects.filter(owner=user)
        return queryset


class LinkUpdateAPIView(UpdateAPIView):
    serializer_class = LinkSerializer
    lookup_field = 'code'
    lookup_url_kwarg = 'code'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = Link.objects.filter(owner=user).order_by('-updated')
        return queryset


class LinkDeleteAPIView(DestroyAPIView):
    serializer_class = LinkSerializer
    lookup_field = 'code'
    lookup_url_kwarg = 'code'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = Link.objects.filter(owner=user).order_by('-updated')
        return queryset


class AboutAPIView(TemplateView):
    template_name = "shortener/api.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain = get_current_site(self.request)
        protocol = 'https' if self.request.is_secure() else 'http'
        context['base_url'] = f'{protocol}://{domain}/api/'
        return context

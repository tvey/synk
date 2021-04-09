import re

from rest_framework import serializers

from shortener.models import Link


class LinkCreateSerializer(serializers.ModelSerializer):
    link = serializers.URLField(required=False)

    class Meta:
        model = Link
        lookup_field = 'code'
        fields = [
            'code',
            'link',
            'source',
        ]
        read_only = ['owner']

    def create(self, validated_data):
        request = self.context.get('request')
        instance, created = Link.objects.get_or_create(**validated_data)
        return instance


class LinkSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    clicks = serializers.SerializerMethodField()
    source = serializers.URLField(required=False)

    class Meta:
        model = Link
        lookup_field = 'code'
        fields = [
            'link',
            'source',
            'code',
            'name',
            'clicks',
            'updated',
            'created',
        ]
        read_only = ['owner', 'link', 'clicks', 'updated', 'created']

    def validate_source(self, value):
        request = self.context.get('request')
        pattern = r'(https?://)?{site}'
        match = re.match(pattern.format(site=request.get_host()), value)
        if match:
            raise serializers.ValidationError('Cannot squeeze self.')
        return value

    def get_link(self, obj):
        request = self.context.get('request')
        protocol = 'https' if request.is_secure() else 'http'
        return f'{protocol}://{request.get_host()}/{obj.code}/'

    def get_clicks(self, obj):
        return obj.click_set.count()


class LinkListSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ['link', 'code', 'source', 'name']

    def get_link(self, obj):
        request = self.context.get('request')
        protocol = 'https' if request.is_secure() else 'http'
        return f'{protocol}://{request.get_host()}/{obj.code}'

from rest_framework import serializers
from .models import AccessToken

class AccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessToken
        fields = ['access_token', 'created_at', 'scanner_name', 'scanner_uid']

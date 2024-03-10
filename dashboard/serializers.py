from rest_framework import serializers
from .models import Sapien, Item

class SapienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sapien
        fields = ['serial_id', 'insti_id', 'name', 'allowed']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['serial_id', 'name', 'category', 'is_available']

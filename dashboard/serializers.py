from rest_framework import serializers
from .models import Sapien, Item, IssueRecord, Bucket

class SapienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sapien
        fields = ['serial_id', 'insti_id', 'name', 'allowed','id']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['serial_id', 'name', 'category', 'is_available','id']

class AddIssueRecordSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    sapien_id = serializers.CharField()

class ReturnItemSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    sapien_id = serializers.CharField()

class BucketSerializer(serializers.ModelSerializer):
    total_count = serializers.IntegerField()
    issued_count = serializers.IntegerField()

    class Meta:
        model = Bucket
        fields = ['bucket_name', 'total_count', 'issued_count', 'id']

class BucketItemsSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Bucket
        fields = ['bucket_name', 'items']

class ItemActivitySerializer(serializers.ModelSerializer):
    user = SapienSerializer() 
    class Meta:
        model = IssueRecord
        fields = [ 'item', 'user', 'issue_time', 'expected_return', 'return_time', 'is_returned']

class SapienActivitySerializer(serializers.ModelSerializer):
    item = serializers.CharField(source='item.name', read_only=True)
    class Meta:
        model = IssueRecord
        fields = [ 'item', 'user', 'issue_time', 'expected_return', 'return_time', 'is_returned']
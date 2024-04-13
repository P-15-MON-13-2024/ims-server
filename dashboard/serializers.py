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
    item_serial_id = serializers.CharField(source='item.serial_id', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    user_details = SapienSerializer(source='user', read_only=True)

    class Meta:
        model = IssueRecord
        fields = ['item', 'item_serial_id', 'item_name', 'user', 'user_details', 'issue_time', 'expected_return', 'return_time', 'is_returned']


class SapienActivitySerializer(serializers.ModelSerializer):
    item_serial_id = serializers.CharField(source='item.serial_id', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = IssueRecord
        fields = ['user', 'user_name', 'item_serial_id', 'item_name', 'issue_time', 'expected_return', 'return_time', 'is_returned']



class IssuedItemSerializer(serializers.ModelSerializer):
    item_serial_id = serializers.CharField(source='item.serial_id', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    user_serial_id = serializers.CharField(source='user.serial_id', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = IssueRecord
        fields = ['item', 'item_serial_id', 'item_name', 'user', 'user_serial_id', 'user_name', 'issue_time', 'expected_return']


class RecentActivitySerializer(serializers.ModelSerializer):
    item_serial_id = serializers.CharField(source='item.serial_id', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_serial_id = serializers.CharField(source='user.serial_id', read_only=True)
    user_insti_id = serializers.CharField(source='user.insti_id', read_only=True)

    class Meta:
        model = IssueRecord
        fields = ['item_serial_id', 'item_name', 'user_name', 'user_serial_id', 'user_insti_id', 'issue_time', 'expected_return', 'return_time', 'is_returned']

class SapienCSVSerializer(serializers.Serializer):
    csv_file = serializers.FileField()
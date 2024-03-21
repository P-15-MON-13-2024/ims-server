from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bucket, Sapien, Item, IssueRecord
from .serializers import BucketSerializer, SapienSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound



@api_view(['GET'])
def list_buckets(request):
    if request.method == 'GET':
        buckets = Bucket.objects.all()
        serializer = BucketSerializer(buckets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_sapiens(request):
    if request.method == 'GET':
        sapiens = Sapien.objects.all()
        serializer = SapienSerializer(sapiens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def list_items(request):
    if request.method == 'GET':
        items_data = []
        buckets = Bucket.objects.all()
        
        # Iterate over each bucket
        for bucket in buckets:
            items = Item.objects.filter(category=bucket)
            for item in items:
                # Get the latest issue record for the item
                latest_issue_record = IssueRecord.objects.filter(item=item, is_returned=False).order_by('-issue_time').first()
                
                # Check if the item is available
                if latest_issue_record is None or latest_issue_record.is_returned:
                    item_data = {
                        'item_id': item.id,
                        'item_name': item.name,
                        'bucket_name': bucket.bucket_name,
                        'availability': 'Available',
                        'latest_issue_time': None,
                        'latest_issued_to': None,
                        'latest_issued_to_serial_id': None
                    }
                else:
                    item_data = {
                        'item_id': item.id,
                        'item_name': item.name,
                        'bucket_name': bucket.bucket_name,
                        'availability': 'Not Available',
                        'latest_issue_time': latest_issue_record.issue_time,
                        'latest_issued_to': latest_issue_record.user.name,
                        'latest_issued_to_serial_id': latest_issue_record.user.serial_id
                    }
                items_data.append(item_data)
        
        return Response(items_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_items_in_bucket(request, bucket_name):
    if request.method == 'GET':
        items_data = []
        try:
            # Retrieve the bucket by name
            bucket = Bucket.objects.get(bucket_name=bucket_name)
            
            # Retrieve all items in the specified bucket
            items = Item.objects.filter(category=bucket)
            for item in items:
                # Get the latest issue record for the item
                latest_issue_record = IssueRecord.objects.filter(item=item, is_returned=False).order_by('-issue_time').first()
                
                # Check if the item is available
                if latest_issue_record is None or latest_issue_record.is_returned:
                    item_data = {
                        'item_id': item.id,
                        'serial_id': item.serial_id,
                        'name': item.name,
                        'availability': 'Available',
                        'issued_to': None
                    }
                else:
                    issued_to = {
                        'name': latest_issue_record.user.name,
                        'serial_id': latest_issue_record.user.serial_id
                    }
                    item_data = {
                        'item_id': item.id,
                        'serial_id': item.serial_id,
                        'name': item.name,
                        'availability': 'Not Available',
                        'issued_to': issued_to
                    }
                items_data.append(item_data)
            
            return Response(items_data, status=status.HTTP_200_OK)
        except Bucket.DoesNotExist:
            return Response({'error': 'Bucket not found'}, status=status.HTTP_404_NOT_FOUND)

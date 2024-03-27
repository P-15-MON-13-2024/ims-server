from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bucket, Sapien, Item, IssueRecord
from .serializers import BucketSerializer, ItemSerializer, SapienSerializer, BucketItemsSerializer,ItemActivitySerializer,SapienActivitySerializer, IssuedItemSerializer
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
def list_items_in_bucket(request, bucket_id):
    try:
        bucket = Bucket.objects.get(id=bucket_id)
    except Bucket.DoesNotExist:
        raise NotFound(detail="Bucket not found", code=status.HTTP_404_NOT_FOUND)

    items = Item.objects.filter(category=bucket)  # Ensure correct filtering

    # Pass both bucket and items queryset to the serializer
    serializer = ItemSerializer(items, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def item_activities(request, serial_id):
    try:
        item = Item.objects.get(serial_id=serial_id)
    except Item.DoesNotExist:
        return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    # Query IssueRecord model to find all records related to the item
    issue_records = IssueRecord.objects.filter(item=item)

    # Serialize the issue records
    serializer = ItemActivitySerializer(issue_records, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def sapien_activities(request, serial_id):
    try:
        sapien = Sapien.objects.get(serial_id=serial_id)
    except Sapien.DoesNotExist:
        return Response({"error": "Sapien not found"}, status=status.HTTP_404_NOT_FOUND)

    # Query IssueRecord model to find all records related to the Sapien
    issue_records = IssueRecord.objects.filter(user=sapien).order_by('-issue_time')

    # Serialize the issue records
    serializer = SapienActivitySerializer(issue_records, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def issued_items(request):
    issued_items = IssueRecord.objects.filter(is_returned=False)

    # Serialize the issued items
    serializer = IssuedItemSerializer(issued_items, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
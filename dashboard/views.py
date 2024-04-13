import asyncio
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from imsserver.utils import telebot_notify_async, telebot_notify_sync
from .models import Bucket, Sapien, Item, IssueRecord
from .serializers import BucketSerializer, ItemSerializer, SapienSerializer, BucketItemsSerializer,ItemActivitySerializer,SapienActivitySerializer, IssuedItemSerializer, RecentActivitySerializer,SapienCSVSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.views.decorators.csrf import csrf_exempt
import csv



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
def get_bucket_items(request, bucket_id):
    try:
        bucket = Bucket.objects.get(id=bucket_id)
    except Bucket.DoesNotExist:
        raise NotFound(detail="Bucket not found", code=status.HTTP_404_NOT_FOUND)

    items = Item.objects.filter(category=bucket)  # Ensure correct filtering

    # Initialize a list to hold the serialized items with additional fields
    serialized_items = []

    # Serialize each item with additional fields
    for item in items:
        serialized_item = ItemSerializer(item).data

        # Get the latest issue record for the item
        latest_issue_record = IssueRecord.objects.filter(item=item, is_returned=False).order_by('-issue_time').first()

        # Add additional fields to the serialized item
        if latest_issue_record:
            issued_by = SapienSerializer(latest_issue_record.user).data
            serialized_item['issued_by'] = issued_by
            serialized_item['issue_time'] = latest_issue_record.issue_time
        else:
            serialized_item['issued_by'] = None
            serialized_item['issue_time'] = None

        serialized_items.append(serialized_item)

    return Response(serialized_items, status=status.HTTP_200_OK)



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

    return Response(serializer.data[::-1], status=status.HTTP_200_OK)

@api_view(['GET'])
def recent_activities(request):
    # Query recent IssueRecord objects
    recent_issue_records = IssueRecord.objects.order_by('-issue_time')[:10]  # Example: Get the latest 10 records

    # Serialize the recent IssueRecord objects
    serializer = RecentActivitySerializer(recent_issue_records, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def send_telegram_message(request):
    """
        {
            "insti_id":"instiID",
            "text":"text"
        }
    """
    try:
        if request.method == 'POST':
            data = request.data
            insti_id = data['insti_id']
            text = data['text']
            asyncio.run(telebot_notify_async(insti_id,text))
            return Response({"message":"sent"})
        return Response({"message":"use request method POST"})
    except Exception as e:
        print(e)
        return Response({"message":"some error occurred"})

@api_view(['POST'])
def upload_sapiens_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        sapiens_created = 0
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            for row in csv_reader:
                serial_id = row.get('serial_id')
                insti_id = row.get('insti_id')
                name = row.get('name')
                allowed = row.get('allowed')
                if serial_id and insti_id and name and allowed:
                    # Create Sapien object
                    sapien = Sapien.objects.create(
                        serial_id=serial_id,
                        insti_id=insti_id,
                        name=name,
                        allowed=bool(allowed)
                    )
                    sapiens_created += 1
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        return Response({'message': f'{sapiens_created} Sapien objects created successfully'}, status=201)
    return Response({'error': 'No file found in the request'}, status=400)


@api_view(['POST'])
def upload_items_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']

        items_created = []
        try:
            # Read the CSV file
            reader = csv.DictReader(csv_file)
            for row in reader:
                # Create an Item object for each row in the CSV
                item = Item.objects.create(
                    serial_id=row['serial_id'],
                    name=row['name'],
                    category=row['category'],
                    is_available=bool(row['is_available'])  # Convert 'is_available' to boolean
                )
                items_created.append(item)

            # Serialize the created items
            serializer = ItemSerializer(items_created, many=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Please provide a CSV file"}, status=status.HTTP_400_BAD_REQUEST)
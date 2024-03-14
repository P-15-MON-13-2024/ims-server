from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import AccessToken
from .serializers import AccessTokenSerializer
from .utils import token_required
from dashboard.serializers import AddIssueRecordSerializer, SapienSerializer, ItemSerializer
from dashboard.models import Sapien, Bucket, Item, IssueRecord

students = {
    '6AD2B612' : {'name':'Abhijat Bharadwaj', 'roll':'210020002'},
    '2A94B212' : {'name':'Animesh Kumar', 'roll':'21D070012'}
}

items={
    '4BE6064C':'Wire Stripper'
}

@api_view(['GET'])
@token_required
def mirror(request):
    serial_id = request.query_params.get('serial')
    if serial_id is not None:
        print(serial_id)
        if serial_id in students:
            print(students[serial_id]['name'])
            print(students[serial_id]['roll'])
        elif serial_id in items:
            print(items[serial_id])
        print()
        return JsonResponse({"message":serial_id})
    else: 
        print("something's wrong")
    return JsonResponse({"message":"f"})

@api_view(['GET'])
def get_access_token(request, scanner_uid):
    try:
        access_token_obj = AccessToken.objects.get(scanner_uid=scanner_uid)
        serializer = AccessTokenSerializer(access_token_obj)
        return JsonResponse(serializer.data)
    except AccessToken.DoesNotExist:
        return JsonResponse({"error":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])   
def get_sapien(request):
    serial = request.query_params.get('serial')
    sapien = Sapien.objects.filter(serial_id=serial).first()
    if sapien:
        serializer = SapienSerializer(sapien)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({"error": "Sapien not found"}, status=404)

@api_view(['GET'])
def get_item(request):
    serial = request.query_params.get('serial')
    item = Item.objects.filter(serial_id=serial).first()
    if item:
        serializer = ItemSerializer(item)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({"error": "Item not found"}, status=404)
    
@api_view(['POST'])
def add_issue_record(request):
    if request.method == 'POST':
        serializer = AddIssueRecordSerializer(data=request.data)
        if serializer.is_valid():
            item_id = serializer.validated_data['item_id']
            sapien_id = serializer.validated_data['sapien_id']
            
            try:
                item = Item.objects.get(serial_id=item_id)
                user = Sapien.objects.get(serial_id=sapien_id)
                
                if item.is_available:
                    new_issue_record = IssueRecord(item=item, user=user)
                    new_issue_record.save()

                    # Update item availability
                    item.is_available = False
                    item.save()

                    # Update issued count of the corresponding bucket model
                    item.category.issued_count += 1
                    item.category.save()

                    return JsonResponse({"message":"Issue record added successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({"message":"Item is not available for issue"}, status=status.HTTP_400_BAD_REQUEST)
            except Item.DoesNotExist:
                return JsonResponse({"message":"Item not found"}, status=status.HTTP_404_NOT_FOUND)
            except Sapien.DoesNotExist:
                return JsonResponse({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import AccessToken
from .serializers import AccessTokenSerializer
from .utils import token_required
from dashboard.serializers import SapienSerializer, ItemSerializer
from dashboard.models import Sapien, Bucket, Item, IssueRecord

students = {
    '6AD2B612' : {'name':'Abhijat Bharadwaj', 'roll':'210020002'},
    '2A94B212' : {'name':'Animesh Kumar', 'roll':'21D070012'}
}

items={
    '4BE6064C':'Wire Stripper'
}


def hello(request):
    return JsonResponse({"message":"Hello from Django!"})

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

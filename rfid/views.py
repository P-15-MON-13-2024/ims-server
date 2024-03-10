from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import AccessToken
from .serializers import AccessTokenSerializer

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
        return Response(serializer.data)
    except AccessToken.DoesNotExist:
        return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

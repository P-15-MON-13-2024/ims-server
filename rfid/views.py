from django.http import JsonResponse
from rest_framework.decorators import api_view

def hello(request):
    return JsonResponse({"message":"Hello from Django!"})

@api_view(['GET'])
def mirror(request):
    serial_id = request.query_params.get('serial')

    if serial_id is not None:
        print(serial_id)
        return JsonResponse({"message":serial_id})
    else: 
        print("something's wrong")
    return JsonResponse({"message":"f"})

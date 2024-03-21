from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bucket, Sapien
from .serializers import BucketSerializer, SapienSerializer
from rest_framework import status



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

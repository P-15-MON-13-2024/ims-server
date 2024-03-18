from django.urls import path
from .views import list_buckets,list_sapiens

urlpatterns = [
    path('categories/', list_buckets, name='list_buckets'),
    path('sapiens/', list_sapiens, name='list_sapiens'),
]
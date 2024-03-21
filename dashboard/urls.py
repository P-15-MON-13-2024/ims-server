from django.urls import path
from .views import list_buckets,list_sapiens, list_items,list_items_in_bucket

urlpatterns = [
    path('get-buckets/', list_buckets, name='list_buckets'),
    path('get-sapiens/', list_sapiens, name='list_sapiens'),
    path('get-items/', list_items, name='list_items'),
    path('items/<str:bucket_name>/', list_items_in_bucket, name='list_items_in_bucket'),
]
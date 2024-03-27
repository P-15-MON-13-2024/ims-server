from django.urls import path
from .views import list_buckets,list_sapiens, list_items,get_bucket_items,item_activities, sapien_activities, issued_items

urlpatterns = [
    path('get-buckets/', list_buckets, name='list_buckets'),
    path('get-sapiens/', list_sapiens, name='list_sapiens'),
    path('get-items/', list_items, name='list_items'),
    path('get-bucket-items/<int:bucket_id>/',get_bucket_items, name='get_bucket_items'),
    path('item-activities/<str:serial_id>/', item_activities, name='item_activities'),
    path('sapien-activities/<str:serial_id>/', sapien_activities, name='sapien_activities'),
    path('issued_items/',issued_items, name='issued_items'),
]
from django.urls import path
from .views import list_buckets,list_sapiens, list_items,get_bucket_items,item_activities, sapien_activities, issued_items, recent_activities, send_telegram_message, upload_sapiens_csv, upload_items_csv

urlpatterns = [
    path('get-buckets/', list_buckets, name='list_buckets'),
    path('get-sapiens/', list_sapiens, name='list_sapiens'),
    path('get-items/', list_items, name='list_items'),
    path('get-bucket-items/<int:bucket_id>/',get_bucket_items, name='get_bucket_items'),
    path('item-activities/<str:serial_id>/', item_activities, name='item_activities'),
    path('sapien-activities/<str:serial_id>/', sapien_activities, name='sapien_activities'),
    path('issued-items/',issued_items, name='issued_items'),
    path('recent-activities/', recent_activities, name='recent_activities'),
    path('send-telegram-msg/', send_telegram_message, name="send_telegram_message"),
    path('upload-sapiens-csv/', upload_sapiens_csv, name='upload_sapien_csv'),
    path('upload-items-csv/', upload_items_csv, name='upload_items_csv'),
    
]
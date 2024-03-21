from django.urls import path
from .views import list_buckets,list_sapiens, list_items

urlpatterns = [
    path('buckets/', list_buckets, name='list_buckets'),
    path('sapiens/', list_sapiens, name='list_sapiens'),
    path('items/', list_items, name='list_items'),
]
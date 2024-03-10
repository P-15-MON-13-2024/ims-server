# myapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', hello, name='hello'),
    path('mirror/', mirror, name='hello'),
    path('access-token/<str:scanner_uid>/', get_access_token),
    path('get-sapien/', get_sapien, name='get_sapien'),
    path('get-item/',get_item, name='get_item'),

]

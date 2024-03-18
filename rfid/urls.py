# myapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('access-token/<str:scanner_uid>/', get_access_token),
    path('get-sapien/', get_sapien, name='get_sapien'),
    path('get-item/',get_item, name='get_item'),
    path('add-issue-record/', add_issue_record, name='issue-record'),
    path('return-item/', return_item, name='return-item'),


]

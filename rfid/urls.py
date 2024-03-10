# myapp/urls.py
from django.urls import path
from .views import hello, mirror
from .views import get_access_token

urlpatterns = [
    path('hello/', hello, name='hello'),
    path('mirror/', mirror, name='hello'),
    path('api/access-token/<str:scanner_uid>/', get_access_token),

]

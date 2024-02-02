# myapp/urls.py
from django.urls import path
from .views import hello, mirror

urlpatterns = [
    path('hello/', hello, name='hello'),
    path('mirror/', mirror, name='hello'),

]

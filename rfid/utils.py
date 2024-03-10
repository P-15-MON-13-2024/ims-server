from functools import wraps
from django.http import JsonResponse
from .models import AccessToken

def verify_access_token(view_func):
    @wraps(view_func)
    def _wrapper(request, *args, **kwargs):
        access_token = request.headers.get('Authorization').split(' ')[1]
        if not AccessToken.objects.filter(token=access_token).exists():
            return JsonResponse({'error': 'Invalid access token'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapper

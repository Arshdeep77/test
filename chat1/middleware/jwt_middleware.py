from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from loguru import logger
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
class SimpleJWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.path.startswith('/auth/'):
            return self.get_response(request)
        
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        auth = authorization.split()

        if not auth or auth[0].lower() != 'bearer':
            return self.get_response(request)

        if len(auth) == 1:
            return JsonResponse({'error': 'Invalid Authorization header. No credentials provided.'}, status=400)
        elif len(auth) > 2:
            return JsonResponse({'error': 'Invalid Authorization header. Credentials string should not contain spaces.'}, status=400)
        decoded_token=None
        try:
            token_string=auth[1]
            decoded_token = jwt.decode(token_string, options={"verify_signature": False})
            
        except TokenError as e:
            return JsonResponse({'error': str(e)}, status=403)
            
        try:
            UntypedToken(auth[1])
        except TokenError as e:
            if decoded_token:
                user_to_deactivate = User.objects.get(id=decoded_token['user_id'])
                print(user_to_deactivate.is_active)
                user_to_deactivate.is_active = False
                user_to_deactivate.save()
            return JsonResponse({'error': str(e)}, status=403)

        return self.get_response(request)


import jwt
from django.conf import settings
from django.http import JsonResponse

class TokenValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path matches the routes where you want to apply the middleware
       
        if request.path.startswith('/pools/execute') or request.path.startswith('/pools/user'):
            # Get the token from the Authorization header
            token = request.headers.get('Authorization')
        
            if not token:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)
            request.userEmail= decoded_token['email']
            response = self.get_response(request)
            return response
        else:
            response = self.get_response(request)
            return response


     
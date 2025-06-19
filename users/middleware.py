import geoip2.database
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .models import ExpireToken  
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
# from datetime import timezone
from django.utils import timezone


from .models import ExpireToken 
from .utils import ExpireTokenAuthentication


class RequestInfoMiddleware(MiddlewareMixin):
    def process_request(self, request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR', '')
        
        user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')

        latitude = longitude = city = country = 'unknown'
        try:
            reader = geoip2.database.Reader('geoip/GeoLite2-City.mmdb')
            response = reader.city(ip)
            latitude = response.location.latitude
            longitude = response.location.longitude
            city = response.city.name
            country = response.country.name
            reader.close()
            
        except Exception as e:
            print(f"GeoIP Lookup Error: {e}")

        # Print Request Info
        print("\n--- Incoming Request Info ---")
        print(f"IP Address  : {ip}")
        print(f"Latitude    : {latitude}")
        print(f"Longitude   : {longitude}")
        print(f"City        : {city}")
        print(f"Time        : {timezone.now()}")
        print(f"Country     : {country}")
        print(f"User-Agent  : {user_agent}")
        print(f"Method      : {request.method}")
        print(f"Path        : {request.path}")
        print(f"Query Params: {request.GET.dict()}")
        print("-----------------------------\n")
 


class TokenExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token and token.startswith('Token '):
        
            raw_token = token.split(' ')[1]
            try:
                user_token = ExpireToken.objects.get(key=raw_token)
                if hasattr(user_token, 'is_expire') and user_token.is_expire():
                    return JsonResponse({'message': 'Token Expired'}, status=401)
            except ExpireToken.DoesNotExist:
                return JsonResponse({'message': 'Invalid Token'}, status=401)
        
        return self.get_response(request)

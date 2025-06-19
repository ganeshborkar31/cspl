from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser,ExpireToken

class ExpireTokenAuthentication(TokenAuthentication):
    model = ExpireToken
    
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if token.is_expire():
            raise AuthenticationFailed('Token has expired')
        return user, token
    
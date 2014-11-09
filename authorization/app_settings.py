'''
Created on Nov 8, 2014

@author: nanaya
'''
from django.conf import settings

from authorization.serializers import (
    TokenSerializer as DefaultTokenSerializer,
    UserDetailsSerializer as DefaultUserDetailsSerializer,
    SignupSerializer as DefaultSignupSerializer,
    LoginSerializer as DefaultLoginSerializer,
    PasswordResetSerializer as DefaultPasswordResetSerializer,
    PasswordResetConfirmSerializer as DefaultPasswordResetConfirmSerializer,
    PasswordChangeSerializer as DefaultPasswordChangeSerializer)
from utils import import_callable


auth = getattr(settings, 'AUTHORIZATION', {})
serializers = auth.get('SERIALIZERS', {})
model_extensions = auth.get('USER_MODEL_EXTENSIONS', [])
auth_model_extensions = [import_callable(e) for e in model_extensions]

TokenSerializer = import_callable(
    serializers.get('TOKEN_SERIALIZER', DefaultTokenSerializer))

UserDetailsSerializer = import_callable(
    serializers.get('USER_DETAILS_SERIALIZER', DefaultUserDetailsSerializer)
)

SignupSerializer = import_callable(
    serializers.get('SIGNUP_SERIALIZER', DefaultSignupSerializer)
)

LoginSerializer = import_callable(
    serializers.get('LOGIN_SERIALIZER', DefaultLoginSerializer)
)

PasswordResetSerializer = import_callable(
    serializers.get('PASSWORD_RESET_SERIALIZER',
        DefaultPasswordResetSerializer)
)

PasswordResetConfirmSerializer = import_callable(
    serializers.get('PASSWORD_RESET_CONFIRM_SERIALIZER',
        DefaultPasswordResetConfirmSerializer)
)

PasswordChangeSerializer = import_callable(
    serializers.get('PASSWORD_CHANGE_SERIALIZER',
        DefaultPasswordChangeSerializer)
)

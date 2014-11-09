'''
Created on Nov 8, 2014

@author: nanaya
'''

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .app_settings import (UserDetailsSerializer, SignupSerializer,
                           LoginSerializer, PasswordResetSerializer,
                           PasswordResetConfirmSerializer,
                           PasswordChangeSerializer, auth_model_extensions)


class Signup(generics.GenericAPIView):

    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            response_serializer = \
                UserDetailsSerializer(self.object, context={'request': request})
            return Response(response_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def post_save(self, obj, created=False):
        if created:
            Token.objects.get_or_create(user=obj)
            for Model in auth_model_extensions:
                Model.objects.create(user=obj)


class Login(generics.GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.

    Accept the following POST parameters: phone_number, password
    Return the full user object.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            Token.objects.get_or_create(user=user)
            response_serializer = \
                UserDetailsSerializer(user, context={'request': request})
            return Response(response_serializer.data,
                            status=status.HTTP_200_OK)
        return Response(self.serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    """
    delete the Token object assigned to the current User object.

    Accepts/Returns nothing.
    """
    permissions_classes = (AllowAny,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)


class PasswordChange(generics.GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"success": "New password has been saved."})


class PasswordReset(generics.GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: phone_number
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)


class PasswordResetConfirm(generics.GenericAPIView):
    """
    Password reset verify number is entered, therefore this resets the user's password.

    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

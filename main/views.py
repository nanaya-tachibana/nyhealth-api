from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

import models
import serializers

from settings.models import Setting


class UserViewSet(viewsets.ModelViewSet):
    """
    User view set.
    """
    model = models.User
    queryset = model.objects.all()
    serializer_class = serializers.UserSerializer

    def list(self, request, *args, **kwargs):
#        if not request.user.is_staff:
#            raise PermissionDenied(
#                detail="You do not have permission to perform this action.")
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def post_save(self, obj, created=False):
        if created:
            Token.objects.create(user=obj)
            Setting.objects.create(user=obj)


class GetAuthTokenAndUserInformation(ObtainAuthToken):
    throttle_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            user = serializer.object['user']
            user = serializers.UserSerializer(user, 
                                              context={'request': self.request})
            return Response(user.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

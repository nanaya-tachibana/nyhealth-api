from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework import permissions
from rest_condition import ConditionalPermission, C, And, Or, Not
from main.permissions import (CreationFree, IsOwner)

from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import PermissionDenied
import models
import serializers

from settings.models import Setting
from vitals.serializers import UserVitalRecordSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    User view set.
    """
    model = models.User
    queryset = model.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [ConditionalPermission, ]
    permission_condition = (C(CreationFree)
                            | (C(permissions.IsAuthenticated) & IsOwner))

    def list(self, request, *args, **kwargs):
#        if not request.user.is_staff:
#            raise PermissionDenied(
#                detail="You do not have permission to perform this action.")
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def post_save(self, obj, created=False):
        if created:
            Token.objects.create(user=obj)
            Setting.objects.create(user=obj)

    @detail_route(methods=['get'])
    def vitals(self, request, pk=None):
        user = self.get_object()
        care_list = [r.user for r in user.care_whom.all()]

        if self.request.user == user or self.request.user in care_list:
            serializer = UserVitalRecordSerializer(user.vitals.all(), 
                                                   context={'request': request},
                                                   many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied(
                    detail="You do not have permission to perform this action.")


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

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
from utils import strtime_to_datetime

from settings.models import Setting
from vitals.serializers import UserVitalRecordSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    User view set.
    """
    model = models.User
    queryset = model.objects.all()
    serializer_class = serializers.UserSerializer
    serializer_fields = ('url', 'auth_token', 'username', 'phone_number',
                         'settings', 'care_relations',
                         'outgoing_care_relations', 'incoming_care_relations',
                         'monitorings')
    permission_classes = [ConditionalPermission, ]
    permission_condition = (C(CreationFree)
                            | (C(permissions.IsAuthenticated) & IsOwner))

    def list(self, request, *args, **kwargs):
#        if not request.user.is_staff:
#            raise PermissionDenied(
#                detail="You do not have permission to perform this action.")
        self.serializer_class = serializers.UserPublicSerializer
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def post_save(self, obj, created=False):
        if created:
            Token.objects.create(user=obj)
            Setting.objects.create(user=obj)

    @detail_route(methods=['get'])
    def vitals(self, request, pk=None):
        since = request.QUERY_PARAMS.get('since', None)
        if since is not None:
            since = strtime_to_datetime(since)

        user = self.get_object()
        care_list = [r.user for r in user.care_whom.all()]

        if self.request.user == user or self.request.user in care_list:
            records = user.vitals
            if since is not None:
                records = records.filter(created__gt=since).all()
            serializer = UserVitalRecordSerializer(
                            records.all(),
                            context={'request': request},
                            many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied(
                    detail="You do not have permission to perform this action.")

    @list_route(methods=['get'])
    def search(self, request):
        username = request.QUERY_PARAMS.get('username', None)
        phone_number = request.QUERY_PARAMS.get('phone_number', None)

        search_users = self.get_queryset()
        if username is not None:
            search_users = search_users.filter(username=username)
        if phone_number is not None:
            search_users = search_users.filter(phone_number=phone_number)

        # only url, name and settings can be seen
        self.serializer_class = serializers.UserPublicSerializer

        page = self.paginate_queryset(search_users)
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)


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

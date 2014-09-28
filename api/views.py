from django.http import Http404
from django.utils.datastructures import MultiValueDict
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import exceptions
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token

from main import models
from api import serializers
from api.permissions import (IsOwner, IsOwnerOrCreationOnly,
                             IsAdminUserOrReadOnly)


class ViewSetWithCareListPermission(viewsets.ModelViewSet):
    """
    Hack viewsets class to allow users caring each other access other's data.
    """

    def check_permissions(self, request):
        in_care_list = True
        if request.method in permissions.SAFE_METHODS:
            try:
                user_id = (self.kwargs.get('user_id', None) or
                    self.kwargs.get('pk', None))
                user = models.User.objects.get(pk=user_id)
                if not (user is None or user.in_care_list(request.user.pk)):
                    in_care_list = False
            except:
                return Response({'detail': 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)

        if not in_care_list:
            super(ViewSetWithCareListPermission, self).check_permissions(request)


class VitalSignViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAdminUserOrReadOnly,)

    model = models.VitalSign
    queryset = model.objects.all()
    serializer_class = serializers.VitalSignSerializer


class UserViewSet(ViewSetWithCareListPermission):
    """
    User view set.
    """
    permission_classes = (IsOwnerOrCreationOnly,)

    model = models.User
    queryset = model.objects.all()
    serializer_class = serializers.UserSerializer

    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                detail="You do not have permission to perform this action.")
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def post_save(self, obj, created=False):
        if created:
            Token.objects.create(user=obj)


class UserSettingsViewSet(viewsets.ModelViewSet):

    permission_classes = (IsOwner, )

    queryset = models.UserSetting.objects.all()
    serializer_class = serializers.UserSettingSerializer
    lookup_field = 'user_id'

    def pre_save(self, obj):
        obj.user = self.request.user


class UserVitalViewSet(ViewSetWithCareListPermission):

    model = models.UserVital
    lookup_field = 'user_id'
    serializer_class = serializers.UserVitalSerializer

    permission_classes = (IsOwner, )

    def get_queryset(self):
        try:
            queryset = self.model.objects.filter(user_id=self.kwargs['user_id'])
            pk = self.kwargs.get('pk', None)
            if pk is not None:
                queryset = queryset.filter(pk=pk)
            until = self.request.QUERY_PARAMS.get('until', None)
            if until is not None:
                queryset = queryset.filter(updated__gt=until)
            return queryset
        except:
            raise Http404

    def pre_save(self, obj):
        obj.user = self.request.user


class UserCaredVitalViewSet(viewsets.ModelViewSet):

    model = models.UserCaredVital
    lookup_field = 'user_id'
    serializer_class = serializers.UserCaredVitalSerializer

    permission_classes = (IsOwner, )

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.kwargs['user_id'])
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        return queryset

    def pre_save(self, obj):
        obj.user = self.request.user


###############################################################################
#  user care-relations views
###############################################################################
class UserCareRelationViewSet(viewsets.ModelViewSet):

    model = models.CareRelation
    lookup_field = 'user_id'
    serializer_class = serializers.CareRelationSerializer

    permission_classes = (IsOwner, )

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.kwargs['user_id'],
                                             opposite__gt=0)
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        return queryset

    def post_delete(self, obj):
        opposite = obj.get_opposite()
        if opposite is not None:
            opposite.delete()


class UserOutgoingCareRelationViewSet(viewsets.ModelViewSet):

    model = models.CareRelation
    lookup_field = 'user_id'
    serializer_class = serializers.OutgoingCareRelationSerializer

    permission_classes = (IsOwner, )

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.kwargs['user_id'],
                                             opposite=0)
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        return queryset

    def create(self, request, *args, **kwargs):
        data = MultiValueDict(request.DATA)
        data['user'] = self.request.user.pk
        serializer = self.get_serializer(data=data, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post_save(self, obj, created=False):
        if created:
            opposite = self.model(user_id=obj.to_user_id,
                                  to_user_id=obj.user_id,
                                  opposite=-1)
            opposite.save()

    def post_delete(self, obj):
        opposite = obj.get_opposite(-1)
        if opposite is not None:
            opposite.delete()


class UserIncomingCareRelationViewSet(viewsets.ModelViewSet):

    model = models.CareRelation
    lookup_field = 'user_id'
    serializer_class = serializers.IncomingCareRelationSerializer

    permission_classes = (IsOwner, )

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.kwargs['user_id'],
                                             opposite=-1)
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        return queryset

    def allow(self, request, *args, **kwargs):
        incoming = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        incoming.allow()
        return Response(status=status.HTTP_200_OK)

    def deny(self, request, *args, **kwargs):
        incoming = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        incoming.deny()
        return Response(status=status.HTTP_204_NO_CONTENT)

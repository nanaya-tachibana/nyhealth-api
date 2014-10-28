from django.utils.datastructures import MultiValueDict
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_condition import ConditionalPermission, C, And, Or, Not
from main.permissions import IsOwner, IsAdminUserOrReadOnly

import models
import serializers
from main.utils import strtime_to_datetime


class MultiCreateModelViewset(viewsets.ModelViewSet):
    """
    Override the create method to support multiply instances creation.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA,
                                         files=request.FILES, many=True)
        if serializer.is_valid():
            [self.pre_save(obj) for obj in serializer.object]
            self.objects = serializer.save(force_insert=True)
            [self.pre_save(obj) for obj in self.objects]
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VitalSignViewSet(MultiCreateModelViewset):

    model = models.VitalSign
    queryset = model.objects.all()
    serializer_class = serializers.VitalSignSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly, ]


class UserVitalRecordViewSet(MultiCreateModelViewset):

    model = models.UserVitalRecord
    serializer_class = serializers.UserVitalRecordSerializer

    permission_classes = [ConditionalPermission, ]
    permission_condition = (C(permissions.IsAuthenticated) & IsOwner)

    def get_queryset(self):
        since = self.request.QUERY_PARAMS.get('since', None)
        vital = self.request.QUERY_PARAMS.get('vital', None)

        records = self.model.objects.filter(user=self.request.user)
        if since is not None:
            records = records.filter(created__gt=strtime_to_datetime(since))
        if vital is not None:
            records = records.filter(vital_id=vital)

        return records.order_by('-updated')

    def pre_save(self, obj):
        obj.user = self.request.user


class UserMonitoringVitalViewSet(MultiCreateModelViewset):

    model = models.UserMonitoringVital
    serializer_class = serializers.UserMonitoringVitalSerializer

    permission_classes = [ConditionalPermission, ]
    permission_condition = (C(permissions.IsAuthenticated) & IsOwner)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).\
            order_by('-updated')

    def pre_save(self, obj):
        obj.user = self.request.user
from django.utils.datastructures import MultiValueDict
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions
from rest_condition import ConditionalPermission, C, And, Or, Not
from main.permissions import IsOwner, IsInRelationList, IsAdminUserOrReadOnly

import models
import serializers


class VitalSignViewSet(viewsets.ModelViewSet):

    model = models.VitalSign
    queryset = model.objects.all()
    serializer_class = serializers.VitalSignSerializer
    permission_classes = [IsAdminUserOrReadOnly, ]


class UserVitalRecordViewSet(viewsets.ModelViewSet):

    model = models.UserVitalRecord
    serializer_class = serializers.UserVitalRecordSerializer

    permission_classes = [ConditionalPermission, ]
    permission_condition = (C(permissions.IsAuthenticated) & IsOwner)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user


class UserMonitoringVitalViewSet(viewsets.ModelViewSet):

    model = models.UserMonitoringVital
    serializer_class = serializers.UserMonitoringVitalSerializer

    permission_classes = [ConditionalPermission, ]
    permission_condition = (C(permissions.IsAuthenticated) & IsOwner)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user
from rest_framework import viewsets

from rest_framework import permissions
from rest_condition import ConditionalPermission, C, And, Or, Not
from main.permissions import IsOwner

import models
import serializers


class UserSettingsViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.UserSettingSerializer
    model = models.Setting
    permission_classes = [ConditionalPermission, ]
    permission_condition = (C(permissions.IsAuthenticated) & IsOwner)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

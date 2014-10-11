from rest_framework import viewsets
from rest_framework import status

import models
import serializers


class UserSettingsViewSet(viewsets.ModelViewSet):

    permission_classes = ()
    serializer_class = serializers.UserSettingSerializer
    model = models.Setting

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

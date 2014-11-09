from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated

import models
import serializers


class UserSettingsViewSet(viewsets.ModelViewSet):

    model = models.Profile
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

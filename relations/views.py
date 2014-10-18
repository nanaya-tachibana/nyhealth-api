from django.utils.datastructures import MultiValueDict
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import permissions
from rest_condition import ConditionalPermission, C, And, Or, Not
from main.permissions import IsOwner

import models
import serializers


class UserRelationViewSet(viewsets.ModelViewSet):

    model = models.Relation
    serializer_class = serializers.RelationSerializer
    permission_classes = [ConditionalPermission, ]
    permission_condition = (C(permissions.IsAuthenticated) & IsOwner)

    def get_queryset(self):
        return self.model.objects.\
            filter(user=self.request.user, opposite__gt=0).order_by('-updated')

    def post_delete(self, obj):
        opposite = obj.get_opposite()
        if opposite is not None:
            opposite.delete()


class UserOutgoingRelationViewSet(viewsets.ModelViewSet):

    model = models.Relation
    serializer_class = serializers.OutgoingRelationSerializer

    permission_classes = [ConditionalPermission, ]
    permission_condition = (C(permissions.IsAuthenticated) & IsOwner)

    def get_queryset(self):
        return self.model.objects.\
            filter(user=self.request.user, opposite=0).order_by('-updated')

    def create(self, request, *args, **kwargs):
        data = MultiValueDict(request.DATA)
        data['user'] = reverse('user-detail', args=[self.request.user.pk])
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


class UserIncomingRelationViewSet(viewsets.ModelViewSet):

    model = models.Relation
    serializer_class = serializers.IncomingRelationSerializer

    permission_classes = [ConditionalPermission, ]
    permission_condition = (C(permissions.IsAuthenticated) & IsOwner)

    def get_queryset(self):
        return self.model.objects.\
            filter(user=self.request.user, opposite=-1).order_by('-updated')

    def allow(self, request, *args, **kwargs):
        incoming = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        incoming.allow()
        return Response(status=status.HTTP_200_OK)

    def deny(self, request, *args, **kwargs):
        incoming = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        incoming.deny()
        return Response(status=status.HTTP_204_NO_CONTENT)

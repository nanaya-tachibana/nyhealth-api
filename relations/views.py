from rest_framework.compat import urlparse
from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated 

from filters import OrderingFilter

import models
import serializers


class UserRelationViewSet(viewsets.ModelViewSet):

    model = models.Relation
    serializer_class = serializers.RelationSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (OrderingFilter,)
    ordering_fields = ('created', 'update')
    ordering = ('-created',)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, opposite__gt=0)

    def post_delete(self, obj):
        obj.destroy()


class UserOutgoingRelationViewSet(viewsets.ModelViewSet):

    model = models.Relation
    serializer_class = serializers.OutgoingRelationSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (OrderingFilter,)
    ordering_fields = ('created', 'update')
    ordering = ('-created',)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, opposite=0)

    def send_request(self, request, *args, **kwargs):
        """
        Send an outgoing request.
        """
        data = dict(request.DATA)
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
            opposite = self.model(user=obj.to_user, to_user=obj.user,
                                  opposite=-1)
            opposite.save()

    def post_delete(self, obj):
        obj.destroy()


class UserIncomingRelationViewSet(viewsets.ModelViewSet):

    model = models.Relation
    serializer_class = serializers.IncomingRelationSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (OrderingFilter,)
    ordering_fields = ('created', 'update')
    ordering = ('-created',)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, opposite=-1)

    def allow(self, request, *args, **kwargs):
        """
        Allow an incoming request.
        """
        incoming = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        incoming.allow()
        return Response(status=status.HTTP_200_OK)

    def deny(self, request, *args, **kwargs):
        """
        Deny an incoming request.
        """
        incoming = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        incoming.deny()
        return Response(status=status.HTTP_204_NO_CONTENT)

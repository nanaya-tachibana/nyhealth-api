from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.decorators import detail_route, list_route

from filters import OrderingFilter, SearchFilter
from permissions import IsAdminUserOrReadOnly, IsOwnerOrHasRelation
from utils import three_month_ago

import models
import serializers


class MultiCreateModelViewset(viewsets.ModelViewSet):
    """
    Override the create method to support multiple instances creation.
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
    permission_classes = (IsAuthenticated, IsAdminUserOrReadOnly, )
    filter_backends = (OrderingFilter,)
    ordering_fields = ('created', 'updated',)
    ordering = ('-created', )

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()), many=True)
        return Response(serializer.data)


class UserVitalRecordViewSet(MultiCreateModelViewset):

    model = models.UserVitalRecord
    serializer_class = serializers.UserVitalRecordSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrHasRelation)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = (('>created', 'since'), ('=vital_id', 'vital'))
    ordering_fields = ('created', 'updated',)
    ordering = ('-created', )

    def custom_object_permission_on_list(self, queryset):
        if queryset:
            user = queryset.all()[0].user
            request_user = self.request.user
            if not (user == request_user or
                    request_user in [r.to_user for r in
                                     user.relations.filter(opposite__gt=0)]):
                detail = "You do not have permission to perform this action."
                raise PermissionDenied(detail=detail)

    def get_queryset(self):
        user_id = self.request.QUERY_PARAMS.get('user', None)
        if user_id is None:
            user_id = self.request.user.pk
        queryset = self.model.objects.filter(user_id=user_id)
        self.custom_object_permission_on_list(queryset)

        # default return records create from 3 month ago to now
        since = self.request.QUERY_PARAMS.get('since', None)
        if since is None:
            queryset = queryset.filter(
                created__gt=three_month_ago().isoformat())
        return queryset

    @list_route(methods=['get'])
    def one_page(self, request):
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()), many=True)
        return Response(serializer.data)

    def pre_save(self, obj):
        obj.user = self.request.user


class UserMonitoringVitalViewSet(MultiCreateModelViewset):

    model = models.UserMonitoringVital
    serializer_class = serializers.UserMonitoringVitalSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (OrderingFilter,)
    ordering_fields = ('created', 'updated',)
    ordering = ('-created', )

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user
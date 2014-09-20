from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.exceptions import ParseError, APIException, PermissionDenied
from rest_framework.authtoken.models import Token


from main import models
from api import serializers
from api.permissions import IsOwnerOrReadOnly
from django.core.context_processors import request
from django.utils.datastructures import MultiValueDict
from mercurial.posix import isowner
from rest_framework.permissions import IsAdminUser


# def parse_request_data(request, fields=None):
#     """
#     Parse the request body.
#     """
#     #  no field is required.
#     if fields is None:
#         try:
#             return request.DATA
#         except ParseError:
#             return {}
# 
#     try:
#         data = request.DATA
#         #  check if any required field is None.
#         data = [data.get(field, None) for field in fields]
#         none_fields = []
#         for (f, d) in zip(fields, data):
#             if d is None:
#                 none_fields.append(f)
#         if none_fields:
#             raise FieldIsRequired(fields=none_fields)
# 
#         return dict(zip(fields, data))
#     except ParseError:
#         raise FieldIsRequired(fields=fields)
# 
# 
# class FieldIsRequired(APIException):
#     status_code = 400
# 
#     def __init__(self, fields, msg=None):
#         msg = msg or 'This field is required.'
#         self.detail = {field: [msg] for field in fields}


class IsOwner(permissions.BasePermission):

    def get_user_id(self, view):
        user_id = view.kwargs.get('user_id', None)
        if user_id is None:
            user_id = view.kwargs.get('pk')
        if user_id is not None:
            user_id = int(user_id)
        return user_id

    def has_permission(self, request, view):
        user_id = self.get_user_id(view)
        return user_id is None or user_id == request.user.id


class IsOwnerOrInCareListReadOnly(IsOwner):

    def has_permission(self, request, view):
        if super(IsOwnerOrInCareListReadOnly, self).has_permission(request, view):
            return True
        elif request.method in permissions.SAFE_METHODS:
            user = models.User.objects.get(pk=self.get_user_id(view))
            return user is None or user.in_care_list(request.user.pk)

        return False


class IsOwnerOrInCareListReadOnlyOrCreatOnly(IsOwnerOrInCareListReadOnly):

    def has_permission(self, request, view):
        if request.method == 'post':
            return True

        return super(IsOwnerOrInCareListReadOnlyOrCreatOnly, self).\
            has_permission(request, view)


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                super(IsAdminUserOrReadOnly, self).has_permission(request,
                                                                  view))


class VitalSignViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAdminUserOrReadOnly,)

    model = models.VitalSign
    queryset = model.objects.all()
    serializer_class = serializers.VitalSignSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    User view set.
    """
    permission_classes = (IsOwnerOrInCareListReadOnlyOrCreatOnly,)

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


class UserVitalViewSet(viewsets.ModelViewSet):

    model = models.UserVital
    lookup_field = 'user_id'
    lookup_url_field = 'pk'
    serializer_class = serializers.UserVitalSerializer

    permission_classes = (IsOwnerOrInCareListReadOnly, )

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.kwargs['user_id'])
        pk = self.kwargs.get('pk', None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        until = self.request.QUERY_PARAMS.get('until', None)
        if until is not None:
            queryset = queryset.filter(updated__gt=until)
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

# class UserCareRelationList(mixins.ListModelMixin):
#     """
#     List all confirmed CareRelation instances.
#     """
# 
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         return CareRelation.get_confirmed_relations(user_id)
# 
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
# 
# 
# class UserCareRelationDetail(APIView):
#     """
#     Retrieve or delete a confirmed CareRelation instance.
#     """
#     permission_classes = (IsOwner, )
# 
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return get_object_or_404(CareRelation, pk=pk, opposite__gt=0)
# 
#     def get(self, request, *args, **kwargs):
#         serializer = CareRelationDetailSerializer(self.get_queryset())
#         return Response(serializer.data)
# 
#     def delete(self, request, *args, **kwargs):
#         relation = self.get_queryset()
#         relation.destroy()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# 
# 
# class UserCareRelationOutgoingList(mixins.ListModelMixin):
#     """
#     List all outgoing CareRelation instances, or create a new one.
#     """
# 
#     permission_classes = (IsOwner, )
#     serializer_class = CareRelationSummarySerializer
# 
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         return CareRelation.get_outgoing_requests(user_id)
# 
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
# 
#     def post(self, request, *args, **kwargs):
#         data = parse_request_data(request, ['to_user', "description"])
#         data['user'] = self.kwargs['user_id']
# 
#         serializer = self.serializer_class(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({'detail': serializer.errors},
#                         status=status.HTTP_400_BAD_REQUEST)
# 
#     def post_save(self, obj, created=False):
#         if created:
#             opposite = CareRelation.objects.create(user_id=obj.to_user,
#                                                    to_user_id=obj.user_id,
#                                                    opposite=-1)
#             opposite.save()
# 
# 
# 
# class UserCareRelationIncomingList(APIView):
#     """
#     List all incoming CareRelation instances.
#     """
#     model = CareRelation
#     permission_classes = (IsOwner, )
#     serializer_class = CareRelationSummarySerializer
# 
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         return CareRelation.get_incoming_requests(user_id)
# 
#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class(self.get_queryset(), many=True)
#         return Response(serializer.data)
# 
# 
# class UserCareRelationOutgoingDetail(APIView):
#     """
#     Retrieve or delete a outgoing CareRelation instance.
#     """
#     permission_classes = (IsOwner, )
# 
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return get_object_or_404(CareRelation, pk=pk, opposite=0)
# 
#     def get(self, request, *args, **kwargs):
#         serializer = CareRelationDetailSerializer(self.get_queryset())
#         return Response(serializer.data)
# 
#     def delete(self, request, *args, **kwargs):
#         relation = self.get_queryset()
#         relation.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# 
# 
# class UserCareRelationIncomingDetail(APIView):
#     """
#     Retrieve or comfirm an incoming CareRelation instance.
#     """
#     permission_classes = (IsOwner, )
# 
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         return get_object_or_404(CareRelation, pk=pk, opposite=-1)
# 
#     def get(self, request, *args, **kwargs):
#         serializer = CareRelationDetailSerializer(self.get_queryset())
#         return Response(serializer.data)
# 
#     def put(self, request, *args, **kwargs):
#         data = parse_request_data(request, ['action'])
#         action = str(data['action']).lower()
# 
#         incoming = self.get_queryset()
#         if action == 'allow':
#             incoming.allow()
#             return Response(status=status.HTTP_201_CREATED)
#         elif action == 'deny':
#             incoming.deny()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             raise FieldIsRequired(fields=['action'],
#                                   msg='This field should be "allow" or "deny".')

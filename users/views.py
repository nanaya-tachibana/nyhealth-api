from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_condition import ConditionalPermission, C, And, Or, Not

from permissions import IsOwner
from filters import SearchFilter
from authorization.views import Signup
from relations.models import Relation

import models
import serializers


class UserView(generics.RetrieveUpdateDestroyAPIView):

    model = models.User
    queryset = model.objects.all()
    serializer_class = serializers.UserSerializer
    serializer_fields = ('url', 'auth_token', 'username', 'phone_number',
                         'settings', 'care_relations',
                         'outgoing_care_relations', 'incoming_care_relations',
                         'monitorings')
    permission_classes = [ConditionalPermission, ]
    permission_condition = ((C(permissions.IsAuthenticated) & IsOwner), )

#    def vitals(self, request, pk=None):
#        """
#        """
#        since = request.QUERY_PARAMS.get('since', None)
#        vital = self.request.QUERY_PARAMS.get('vital', None)
#        if since is not None:
#            since = strtime_to_datetime(since)
#        else:
#            since = three_month
#
#        user = self.get_object()
#        care_list = [r.to_user for
#                     r in user.relations.filter(opposite__gt=0).all()]
#
#        if self.request.user == user or self.request.user in care_list:
#            records = user.vitals.filter(created__gt=since)
#            if vital is not None:
#                records = records.filter(vital_id=vital)
#            serializer = UserVitalRecordSerializer(
#                            records.all(),
#                            context={'request': request},
#                            many=True)
#            return Response(serializer.data, status=status.HTTP_200_OK)
#        else:
#            raise PermissionDenied(
#                    detail="You do not have permission to perform this action.")

    def pre_delete(self, obj):
        for r in obj.cared_by_whom.all():
            r.destroy()
        for r in obj.care_whom.all():
            r.destroy()
        obj.settings.delete()
        for m in obj.monitorings.all():
            m.delete()


class SearchUser(generics.GenericAPIView):

    model = models.User
    queryset = model.objects.all()
    serializer_class = serializers.UserPublicSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=username', '=phone_number')
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)


class InviteUser(Signup):
    """
    Create a user account which can be used to invite others to use.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post_save(self, obj, created=False):
        Relation.build_relations(self.request.user, obj)
        super(InviteUser, self).post_save(obj, created)

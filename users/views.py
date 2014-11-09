from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from filters import SearchFilter
from authorization.views import Signup
from relations.models import Relation

import models
import serializers


class UserView(generics.RetrieveUpdateDestroyAPIView):

    model = models.User
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def pre_delete(self, obj):
        for r in obj.relations.all():
            r.destroy()
        obj.profiles.delete()
        for m in obj.monitorings.all():
            m.delete()


class SearchUser(generics.GenericAPIView):

    model = models.User
    queryset = model.objects.all()
    serializer_class = serializers.UserPublicSerializer
    filter_backends = (SearchFilter,)
    search_fields = (('=username', 'username'),
                     ('=phone_number', 'phone_number'))
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.filter_queryset(self.get_queryset()))
        serializer = self.get_pagination_serializer(page)
        return Response(serializer.data)


class InviteUser(Signup):
    """
    Create a user account which can be used to invite others to use.
    """
    permission_classes = (IsAuthenticated,)

    def post_save(self, obj, created=False):
        Relation.build_relations(self.request.user, obj)
        super(InviteUser, self).post_save(obj, created)

'''
Created on Nov 9, 2014

@author: nanaya
'''
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from filters import OrderingFilter

from .models import Inbox
from .serializers import InboxSerializer


class InboxViewSet(viewsets.ModelViewSet):
    """
    Provides `list` and `read` actions.
    """
    model = Inbox
    serializer_class = InboxSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).\
            order_by('-message__date')

    def read(self, request, *args, **kwargs):
        """
        delete message after reading.
        """
        self.object = self.get_object()
        serializer = self.get_serializer(self.object)
        self.object.destroy()
        return Response(serializer.data)


@permission_classes((IsAuthenticated))
@api_view(['POST'])
def mark_all_read(request):
    """
    Mark all messages as read (i.e. delete from inbox) for current logged in user
    """
    Inbox.delete_all(request.user)
    return Response({"message": "All messages read"})

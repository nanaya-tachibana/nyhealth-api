# -*- coding: utf-8 -*-
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

from main import models


class IsOwner(permissions.BasePermission):
    """
    Only owner has permission to access.
    """
    def get_user_id(self, view):
        user_id = view.kwargs.get('user_id', None) or view.kwargs.get('pk', None)
        if user_id is not None:
            user_id = int(user_id)
        return user_id

    def has_permission(self, request, view):
        user_id = self.get_user_id(view)
        return user_id is None or user_id == request.user.id


class IsOwnerOrCreationOnly(IsOwner):
    """
    Only owner has permission to access, but creation is free.
    """
    def has_permission(self, request, view):
        if request.method == 'post':
            return True

        return super(IsOwnerOrCreationOnly, self).has_permission(request,
                                                                 view)


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                super(IsAdminUserOrReadOnly, self).has_permission(request,
                                                                  view))

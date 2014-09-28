# -*- coding: utf-8 -*-
from api.permissions import IsOwnerOrReadOnly
from django.core.context_processors import request
from django.utils.datastructures import MultiValueDict
from rest_framework.permissions import IsAdminUser


class IsOwner(permissions.BasePermission):
    """
    Only owner has permission to access.
    """
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
    """
    Owner has permission to access 
    and user in one's relation list has read permission.
    """
    def has_permission(self, request, view):
        if super(IsOwnerOrInCareListReadOnly, self).has_permission(request, view):
            return True
        elif request.method in permissions.SAFE_METHODS:
            user = models.User.objects.get(pk=self.get_user_id(view))
            return user is None or user.in_care_list(request.user.pk)

        return False


class IsOwnerOrInCareListReadOnlyOrCreatOnly(IsOwnerOrInCareListReadOnly):
    """
    Owner has permission to access 
    and user in one's relation list has read permission.
    
    Creation is free.
    """
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

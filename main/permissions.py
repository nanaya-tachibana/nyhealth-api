# -*- coding: utf-8 -*-
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

from main import models


class IsOwner(permissions.BasePermission):
    """
    Only owner has permission to access.
    """
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `user`
        return  getattr(obj, 'user', None) == request.user


class CreationFree(permissions.BasePermission):
    """
    Anyone can perform creations.
    """
    def has_permission(self, request, view):
        return request.method == 'POST'


class IsInRelationList(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user in [r.to_user for r in obj.user.care_whom]


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                super(IsAdminUserOrReadOnly, self).has_permission(request,
                                                                  view))

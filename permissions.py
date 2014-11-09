# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

User = get_user_model()


class IsOwnerOrHasRelation(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (request.user == obj.user or
                    request.user in [r.to_user for r in
                                     obj.user.relations.filter(opposite__gt=0)])


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                super(IsAdminUserOrReadOnly, self).has_permission(request,
                                                                  view))

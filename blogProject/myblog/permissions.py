from rest_framework import permissions
from django.contrib.auth.models import User


# class PostListPermission(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         if request


class PostCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.is_authenticated, ' is authenticated')
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

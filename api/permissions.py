from rest_framework import permissions


class ProductPermission(permissions.BasePermission):

    def user_has_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.uid

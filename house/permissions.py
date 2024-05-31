from rest_framework import permissions

class IsHouseManagerOrNone(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
           return True
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.manager == request.user.profilemodel


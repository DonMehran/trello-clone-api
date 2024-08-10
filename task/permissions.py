from rest_framework import permissions


class IsAllowedToEditTaskListElseNone(permissions.BasePermission):

    def has_permission(self, request, view):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # if not request.user.is_anonymous and view:
        #     return True
        #
        # else:
        #     return False
        return not request.user.is_anonymous and view is not None

    def has_object_permission(self, request, view, obj):
        return request.user.profile.house == obj.house


class IsAllowedToEditTaskElseNone(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.profile.house is not None
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.profile.house == obj.task_list.house


class IsAllowedToEditAttachmentElseNone(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.profile.house is not None
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.profile.house == obj.task.task_list.house

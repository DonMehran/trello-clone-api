from rest_framework import permissions

class IsOwnerOrGetAndPostOnly(permissions.BasePermission):
    '''
    CUSTOM PERMISSION CLASS TO ALLOW ONLY GET AND POST REQUESTS OR PUT AND PATCH IF OWNER
    '''
    def has_permission(self, request, view):
        # if request.method in ['GET', 'POST']:
        return True
    
    # if the has permission return false this will not run at all
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_anonymous and request.user == obj:
            return True
        
        return False

from rest_framework import permissions
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj or request.user.is_superuser
        return request.user.is_superuser

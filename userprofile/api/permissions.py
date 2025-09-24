# permissions.py
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
    
        return obj == request.user


class IsAdminOrPostOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True  
        return request.user and request.user.is_staff  
    
class IsBusinessOwnerOrAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type == 'owner' or request.user.is_staff


class ReadOnly(permissions.BasePermission):
   
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
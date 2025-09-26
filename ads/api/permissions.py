
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, 'owner', None) or getattr(obj, 'user', None)
        return owner == request.user


class IsBusinessOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return obj.business.owner == request.user
        except (AttributeError, ObjectDoesNotExist):
            return False

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated
        return True


class IsReviewAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanRedeemPromotion(permissions.BasePermission):
 
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.business.owner != request.user


class CanReportReview(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = obj.business.owner == request.user
        is_admin = request.user.is_staff
        return is_owner or is_admin


class IsAdminOrSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class CanCreatePromotionalContent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.business.owner == request.user
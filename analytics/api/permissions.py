from rest_framework.permissions import BasePermission
from listings.models import BusinessListing


class IsBusinessOwnerOrAdmin(BasePermission):
    def has_permission(self,request,view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        businsess_slug = request.query_params.get('business_slug')
        if businsess_slug:
            return BusinessListing.objects.filter(slug=businsess_slug,
                    owner=request.user).exists()
        return False
    
    def  has_object_permissions(slef,request,view,obj):
        return(
            request.user.is_staff or
            obj.business.owner == request.user
        )

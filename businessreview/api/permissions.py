from rest_framework import permissions

class IsNotBusinessOwner(permissions.BasePermission):
    message = "Business owner cannot review their own business."

    def has_permission(self, request, view):
        if request.method == "POST":
            business_slug = view.kwargs.get('business_slug')
            if business_slug:
                from listings.models import BusinessListing
                from django.shortcuts import get_object_or_404
                business = get_object_or_404(BusinessListing, slug=business_slug)
                return request.user != business.owner
        return True


class IsBusinessOwner(permissions.BasePermission):
    message = "Only the business owner can reply to this review."

    def has_permission(self, request, view):
        if request.method == "POST":
            review = view.get_object()
            return request.user == review.business.owner
        return True


class IsAuthorOfReview(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsOwnerOfReviewReply(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
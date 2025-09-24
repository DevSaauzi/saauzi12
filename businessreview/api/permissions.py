

from rest_framework import permissions
from django.shortcuts import get_object_or_404
from listings.models import BusinessListing


class IsNotBusinessOwner(permissions.BasePermission):
    message = "Business owner cannot review their own business."

    def has_permission(self, request, view):
        if request.method == "POST":
            business_slug = view.kwargs.get('business_slug')
            if business_slug:
                business = get_object_or_404(BusinessListing, slug=business_slug)
                return request.user != business.owner
        return True


class IsReviewAuthor(permissions.BasePermission):
    message = "You cannot report your own review."

    def has_permission(self, request, view):
        if request.method == "POST":
            review = view.get_object()
            return request.user != review.author
        return True


class IsBusinessOwner(permissions.BasePermission):
    message = "Only the business owner can reply to this review."

    def has_permission(self, request, view):
        if request.method == "POST":
            review = view.get_object()
            return request.user == review.business.owner
        return True


class IsOwnerOfReviewReply(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAuthorOfReview(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
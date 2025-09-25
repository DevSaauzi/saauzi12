from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from businessreview.models import Review, ReportedReview, ReviewReply
from listings.models import BusinessListing
from .serializers import ReviewSerializer, ReportedReviewSerializer, ReviewReplySerializer
from .permissions import (
    IsNotBusinessOwner,
    IsBusinessOwner,
    IsAuthorOfReview,
    IsOwnerOfReviewReply
)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('author', 'business').prefetch_related('reports', 'reply')
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'retrieve':
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated(), IsNotBusinessOwner()]
        elif self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsAuthorOfReview()]
        elif self.action == 'destroy':
            return [permissions.IsAdminUser()]
        elif self.action == 'report':
            return [permissions.IsAuthenticated()]
        elif self.action == 'reply':
            return [permissions.IsAuthenticated(), IsBusinessOwner()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        business_slug = self.kwargs.get('business_slug')
        if business_slug:
            return self.queryset.filter(business__slug=business_slug)
        return self.queryset

    def perform_create(self, serializer):
        business_slug = self.kwargs.get('business_slug')
        if not business_slug:
            raise ValueError("Business slug is required.")
        business = get_object_or_404(BusinessListing, slug=business_slug)
        try:
            serializer.save(author=self.request.user, business=business)
        except IntegrityError:
            raise serializers.ValidationError("You have already reviewed this business.")

    @action(detail=True, methods=['post'], url_path='report')
    def report(self, request, pk=None):
        review = self.get_object()
        serializer = ReportedReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(reviewed=review, reported_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='reply')
    def reply(self, request, pk=None):
        review = self.get_object()
        if hasattr(review, 'reply'):
            return Response(
                {"detail": "A reply already exists for this review."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ReviewReplySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(review=review, owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportedReviewViewSet(viewsets.ModelViewSet):
    queryset = ReportedReview.objects.select_related(
        'reviewed__business', 'reported_by', 'resolved_by'
    ).prefetch_related('reviewed__author')
    serializer_class = ReportedReviewSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        if 'status' in serializer.validated_data:
            if serializer.validated_data['status'] != 'pending':
                serializer.save(resolved_by=self.request.user, resolved_at=timezone.now())
            else:
                serializer.save(resolved_by=None, resolved_at=None)
        else:
            serializer.save()


class ReviewReplyViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewReplySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfReviewReply]

    def get_queryset(self):
        return ReviewReply.objects.select_related('review__business', 'owner').filter(owner=self.request.user)

    def perform_create(self, serializer):
        review = serializer.validated_data['review']
        if review.business.owner != self.request.user:
            raise PermissionDenied("You can only reply to your own business reviews.")
        if hasattr(review, 'reply'):
            raise serializers.ValidationError("A reply already exists.")
        serializer.save(owner=self.request.user)
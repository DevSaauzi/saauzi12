# listings/views.py

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch

from listings.models import Category, SubCategory, BusinessListing, BusinessLocation
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    BusinessListingSerializer,
    BusinessLocationSerializer,
)
from .permissions import IsBusinessOwnerOrReadOnly, IsAdminOrReadOnly  


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True).prefetch_related(
        Prefetch('subcategories', queryset=SubCategory.objects.filter(is_active=True))
    )
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    lookup_field = 'slug'


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all() 
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminOrReadOnly]  
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'category__name']
    ordering = ['category__name', 'name']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = SubCategory.objects.filter(is_active=True).select_related('category')
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


class BusinessListingViewSet(viewsets.ModelViewSet):
    queryset = BusinessListing.objects.none() 
    serializer_class = BusinessListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsBusinessOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'subcategory': ['exact'],
        'status': ['exact'],
        'is_featured': ['exact'],
        'verified_badge': ['exact'],
    }
    search_fields = ['name', 'description', 'meta_keywords']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return BusinessListing.objects.select_related(
            'owner', 'category', 'subcategory', 'primary_location'
        ).prefetch_related('locations')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        businesses = self.get_queryset().filter(owner=request.user)
        serializer = self.get_serializer(businesses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        business = self.get_object()
        business.status = 'approved'
        business.rejection_reason = ''
        business.save(update_fields=['status', 'rejection_reason'])
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        business = self.get_object()
        reason = request.data.get('reason', '').strip()
        if not reason:
            return Response({'reason': 'This field is required.'}, status=400)
        business.status = 'rejected'
        business.rejection_reason = reason
        business.save(update_fields=['status', 'rejection_reason'])
        return Response({'status': 'rejected', 'reason': reason})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def feature(self, request, pk=None):
        business = self.get_object()
        business.is_featured = True
        business.save(update_fields=['is_featured'])
        return Response({'is_featured': True})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def unfeature(self, request, pk=None):
        business = self.get_object()
        business.is_featured = False
        business.save(update_fields=['is_featured'])
        return Response({'is_featured': False})

    @action(detail=True, methods=['get'], url_path='locations')
    def list_locations(self, request, pk=None):
        business = self.get_object()
        serializer = BusinessLocationSerializer(business.locations.all(), many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only administrators can delete business listings."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class BusinessLocationViewSet(viewsets.ModelViewSet):
    queryset = BusinessLocation.objects.all() 
    serializer_class = BusinessLocationSerializer
    permission_classes = [permissions.IsAuthenticated, IsBusinessOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        base_qs = BusinessLocation.objects.select_related('business__owner')
        if user.is_staff:
            return base_qs
        return base_qs.filter(business__owner=user)

    def _validate_ownership(self, business):
        if business.owner != self.request.user:
            raise permissions.PermissionDenied("You do not own this business.")

    def perform_create(self, serializer):
        business = serializer.validated_data['business']
        self._validate_ownership(business)
        serializer.save()

    def perform_update(self, serializer):
        self._validate_ownership(serializer.instance.business)
        serializer.save()

    def perform_destroy(self, instance):
        self._validate_ownership(instance.business)
        instance.delete()
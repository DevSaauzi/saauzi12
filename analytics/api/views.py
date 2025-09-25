from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permissions import IsBusinessOwnerOrAdmin  
from analytics.models import BusinessView, WeeklyRanking, MonthlyRanking, ContactClick
from .serializers import (
    BusinessViewSerializer,        
    WeeklyRankingSerializer,
    MonthlyRankingSerializer,
    ContactClickSerializer
)


class BusinessViewViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = BusinessViewSerializer  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        serializer.save(ip_address=ip_address, user_agent=user_agent)

        return Response(
            {"detail": "View tracked successfully."},
            status=status.HTTP_201_CREATED
        )


class ContactClickViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = ContactClickSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip_address = request.META.get('REMOTE_ADDR')
        serializer.save(ip_address=ip_address)

        return Response(
            {"detail": "Contact click tracked successfully."},
            status=status.HTTP_201_CREATED
        )


class WeeklyRankingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeeklyRanking.objects.select_related('business').order_by('-week_start')
    serializer_class = WeeklyRankingSerializer
    permission_classes = [IsBusinessOwnerOrAdmin]  

    def get_queryset(self):
        queryset = super().get_queryset()
        business_slug = self.request.query_params.get('business_slug')
        if business_slug:
            return queryset.filter(business__slug=business_slug)
        return queryset  


class MonthlyRankingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MonthlyRanking.objects.select_related('business').order_by('-year', '-month')
    serializer_class = MonthlyRankingSerializer
    permission_classes = [IsBusinessOwnerOrAdmin]  

    def get_queryset(self):
        queryset = super().get_queryset()
        business_slug = self.request.query_params.get('business_slug')
        if business_slug:
            return queryset.filter(business__slug=business_slug)
        return queryset

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import PermissionDenied

from ads.models import FeaturedListing, BannerAd, Cupon, Flashdeal, AdClick
from .serializers import (
    FeaturedListingSerializer,
    BannerAdSerializer,
    CouponSerializer,
    FlashDealSerializer,
)
from .permissions import (
    IsAdmin,
    IsBusinessOwner,
    CanRedeemPromotion,
    IsAdminOrOwner
)
from listings.models import BusinessListing
from rest_framework.permissions import AllowAny, IsAuthenticated




class FeaturedListingViewSet(viewsets.ModelViewSet):
    queryset = FeaturedListing.objects.select_related('business')
    serializer_class = FeaturedListingSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'approve':
            return [IsAdmin()]
    
        return [IsAdmin()]

    def get_queryset(self):
        if self.action == 'list':
            now = timezone.now()
            return FeaturedListing.objects.filter(
                is_active=True,
                start_date__lte=now,
                end_date__gte=now
            ).select_related('business')
        return FeaturedListing.objects.all()

    def perform_create(self, serializer):
        business = serializer.validated_data['business']
        if business.owner != self.request.user:
            raise PermissionDenied("You can only feature your own business.")
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        featured = self.get_object()
        featured.is_active = True
        featured.save(update_fields=['is_active'])
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)





class BannerAdViewSet(viewsets.ModelViewSet):
    queryset = BannerAd.objects.all()
    serializer_class = BannerAdSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'approve':
            return [IsAdmin()]
        elif self.action == 'click':
            return [AllowAny()]
     
        return [IsAdmin()]

    def get_queryset(self):
        if self.action == 'list':
            now = timezone.now()
            return BannerAd.objects.filter(
                is_active=True,
                start_date__lte=now,
                end_date__gte=now
            )
        return BannerAd.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        ad = self.get_object()
        ad.is_active = True
        ad.save(update_fields=['is_active'])
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def click(self, request, pk=None):
        ad = self.get_object()
        ip = request.META.get('REMOTE_ADDR')
        user = request.user if request.user.is_authenticated else None
        AdClick.objects.create(ad=ad, user=user, ip_address=ip)
        return Response({'clicked': True}, status=status.HTTP_201_CREATED)



class CouponViewSet(viewsets.ModelViewSet):
    queryset = Cupon.objects.all()
    serializer_class = CouponSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'approve':
            return [IsAdmin()]
        elif self.action == 'redeem':
            return [CanRedeemPromotion()]
        return [IsAdmin()] 

    def get_queryset(self):
        if self.action == 'list':
            now = timezone.now()
            return Cupon.objects.filter(
                status='approved',
                valid_from__lte=now,
                valid_until__gte=now,
                is_active=True
            )
        return Cupon.objects.all()

    def perform_create(self, serializer):
        business = serializer.validated_data['business']
        if business.owner != self.request.user:
            raise PermissionDenied("You can only create coupons for your own business.")
        serializer.save(status='pending')

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        coupon = self.get_object()
        coupon.status = 'approved'
        coupon.save(update_fields=['status'])
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[CanRedeemPromotion])
    def redeem(self, request, pk=None):
        coupon = self.get_object()
        if not coupon.is_active:
            return Response({'error': 'Coupon is not active or expired.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            coupon.refresh_from_db()
            if coupon.usage_limit > 0 and coupon.used_count >= coupon.usage_limit:
                return Response({'error': 'Coupon usage limit reached.'}, status=status.HTTP_400_BAD_REQUEST)
            coupon.used_count += 1
            coupon.save(update_fields=['used_count'])
        return Response({'message': 'Coupon redeemed successfully.'}, status=status.HTTP_200_OK)



class FlashDealViewSet(viewsets.ModelViewSet):
    queryset = Flashdeal.objects.all()
    serializer_class = FlashDealSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'approve':
            return [IsAdmin()]
        elif self.action == 'redeem':
            return [CanRedeemPromotion()]
        return [IsAdmin()]

    def get_queryset(self):
        if self.action == 'list':
            now = timezone.now()
            return Flashdeal.objects.filter(
                status='approved',
                starts_at__lte=now,
                ends_at__gte=now,
                is_active=True
            )
        return Flashdeal.objects.all()

    def perform_create(self, serializer):
        business = serializer.validated_data['business']
        if business.owner != self.request.user:
            raise PermissionDenied("You can only create flash deals for your own business.")
        serializer.save(status='pending')

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        deal = self.get_object()
        deal.status = 'approved'
        deal.save(update_fields=['status'])
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[CanRedeemPromotion])
    def redeem(self, request, pk=None):
        deal = self.get_object()
        if not deal.is_active:
            return Response({'error': 'Flash deal is not active.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            deal.refresh_from_db()
            if deal.max_redemptions > 0 and deal.redemptions >= deal.max_redemptions:
                return Response({'error': 'Redemption limit reached.'}, status=status.HTTP_400_BAD_REQUEST)
            deal.redemptions += 1
            deal.save(update_fields=['redemptions'])
        return Response({'message': 'Flash deal redeemed.'}, status=status.HTTP_200_OK)
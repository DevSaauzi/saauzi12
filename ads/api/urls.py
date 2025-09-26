
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()


router.register(r'featured', views.FeaturedListingViewSet, basename='featured')
router.register(r'banner-ads', views.BannerAdViewSet, basename='banner-ad')
router.register(r'promotions', views.CouponViewSet, basename='promotion')
router.register(r'flash-deals', views.FlashDealViewSet, basename='flash-deal')

urlpatterns = [
    path('api/', include(router.urls)),
]
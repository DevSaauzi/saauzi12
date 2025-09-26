from rest_framework import serializers
from ads.models import Cupon,FeaturedListing,BannerAd,Flashdeal



class FeaturedListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedListing
        fields = '__all__'
        read_only_fields = ['is_active', 'created_at']



class BannerAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerAd
        fields = '__all__'



class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        fields = '__all__'
        read_only_fields = ['used_count', 'is_active', 'status', 'rejection_reason']



class FlashDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashdeal
        fields = '__all__'
        read_only_fields = ['redemptions', 'is_active', 'status']
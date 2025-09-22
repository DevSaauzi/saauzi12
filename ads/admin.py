from django.contrib import admin
from .models import FeaturedListing, BannerAd, AdClick, Cupon, Flashdeal  



@admin.register(FeaturedListing)
class FeaturedListingAdmin(admin.ModelAdmin):
    list_display = ['business', 'start_date', 'end_date', 'is_active', 'price']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['business__name', 'business__owner__email']
    readonly_fields = ['created_at']


@admin.register(BannerAd)
class BannerAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'is_active', 'start_date', 'end_date']
    list_filter = ['position', 'is_active', 'start_date', 'end_date']
    search_fields = ['title', 'url']
    readonly_fields = ['created_at']



@admin.register(AdClick)
class AdClickAdmin(admin.ModelAdmin):
    list_display = ['ad', 'user', 'ip_address', 'clicked_at']
    list_filter = ['clicked_at', 'ad', 'user']
    search_fields = ['ad__title', 'user__email', 'ip_address']
    readonly_fields = ['clicked_at']
    date_hierarchy = 'clicked_at'
    ordering = ['-clicked_at']


@admin.register(Cupon) 
class CuponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'valid_form', 'valid_until', 'is_active', 'used_count', 'status']
    list_filter = ['discount_type', 'is_active', 'status', 'valid_form', 'valid_until']
    search_fields = ['code', 'business__name']
    readonly_fields = ['created_at', 'used_count', 'updated_at']
    date_hierarchy = 'valid_form'
    ordering = ['-created_at']


@admin.register(Flashdeal) 
class FlashdealAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_percentage', 'starts_at', 'ends_at', 'is_active', 'status', 'redemptions']
    list_filter = ['is_active', 'status', 'starts_at', 'ends_at']
    search_fields = ['title', 'business__name']
    readonly_fields = ['created_at', 'updated_at', 'redemptions']
    date_hierarchy = 'starts_at'
    ordering = ['-starts_at']
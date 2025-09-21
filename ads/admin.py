
from django.contrib import admin
from .models import FeaturedListing, BannerAd

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






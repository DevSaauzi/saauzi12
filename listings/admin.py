
from django.contrib import admin
from listings.models import Category, SubCategory, BusinessListing,BusinessLocation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(SubCategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']
    ordering = ['category', 'name']


@admin.register(BusinessListing)
class BusinessListingAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'category', 'subcategory', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'category', 'subcategory', 'is_featured', 'owner', 'verified_badge']
    search_fields = ['name', 'description', 'website', 'email', 'phone']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['owner', 'category', 'subcategory', 'primary_location']
    ordering = ['-created_at']

@admin.register(BusinessLocation)
class BusinessLocationAdmin(admin.ModelAdmin):
    list_display = ['business', 'municipality', 'opening_time', 'closing_time']
    list_filter = ['business__category', 'business__subcategory']  
    search_fields = ['business__name', 'municipality', 'street', 'phone']
    autocomplete_fields = ['business']
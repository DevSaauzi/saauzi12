from django.contrib import admin
from listings.models import (
    Category,
    SubCategory,
    BusinessListing,
   
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']  
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubCategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']  
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']


@admin.register(BusinessListing)
class BusinessListingAdmin(admin.ModelAdmin):
    list_display = ['name', 'owners', 'Category', 'SubCategory', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'Category', 'SubCategory', 'is_featured', 'owners']
    search_fields = ['name', 'description', 'social_links', 'website', 'email']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['owners', 'Category', 'SubCategory']  
    def get_list_display(self, request):
        return self.list_display






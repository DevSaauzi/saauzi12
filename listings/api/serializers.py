
from rest_framework import serializers
from listings.models import Category, SubCategory, BusinessListing, BusinessLocation
from userprofile.api.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'is_active', 'subcategories']
        read_only_fields = ['slug', 'created_at', 'updated_at']


class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = SubCategory
        fields = [
            'id', 'category', 'category_name', 'name', 'slug',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
        extra_kwargs = {
            'category': {'write_only': True}
        }


class BusinessLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessLocation
        fields = [
            'id', 'province', 'district', 'municipality',
            'ward', 'street', 'phone', 'email',
            'latitude', 'longitude', 'opening_time', 'closing_time'
        ]


class BusinessListingSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.filter(is_active=True),
        required=True
    )
    
    subcategory = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=SubCategory.objects.filter(is_active=True),
        required=False,
        allow_null=True
    )
    
    subcategory_name = serializers.CharField(
        source='subcategory.name',read_only=True,allow_null=True)
    
    locations = BusinessLocationSerializer(many=True, read_only=True)
    display_status = serializers.CharField(read_only=True)

    class Meta:
        model = BusinessListing
        fields = [
            'id', 'name', 'slug', 'category', 'subcategory', 'subcategory_name',
            'email', 'phone', 'website', 'description', 'social_links',
            'logo', 'cover_image',
            'status', 'display_status', 'rejection_reason',
            'is_featured', 'verified_badge', 'has_multiple_locations',
            'primary_location',
            'meta_title', 'meta_description', 'meta_keywords',
            'owner', 'locations',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'slug', 'status', 'display_status', 'rejection_reason',
            'created_at', 'updated_at', 'owner'
        ]

    def validate(self, data):
        category = data.get('category')
        subcategory = data.get('subcategory')
        if subcategory and category and subcategory.category != category:
            raise serializers.ValidationError({
                'subcategory': f"Subcategory '{subcategory.name}' does not belong to category '{category.name}'."
            })
        return data
    
    
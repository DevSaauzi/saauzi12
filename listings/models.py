
from django.db import models
from userprofile.models import User
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "Subcategories"
        unique_together = ('category', 'name')
        ordering = ['category', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        cat_name = self.category.name if self.category else "Uncategorized"
        return f"{cat_name} → {self.name}"


class BusinessListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('rejected', 'Rejected'),
    ]

    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="businesses",
        help_text="User who owns this business listing",null=True)
    name = models.CharField(max_length=200, help_text="Official business name")
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="URL-friendly version of name")

    category = models.ForeignKey('Category',on_delete=models.PROTECT,related_name="listings",
        help_text="Main category (e.g., Restaurant, Salon)",null=True,blank=True)
    subcategory = models.ForeignKey('SubCategory',on_delete=models.PROTECT,related_name="listings",
        blank=True,null=True,help_text="Specific subcategory (e.g., Italian Restaurant, Hair Salon)")

    phone = models.CharField(max_length=15, blank=True, help_text="Primary contact number")
    email = models.EmailField(max_length=254, blank=True, help_text="Business contact email")
    website = models.URLField(blank=True, help_text="Official website URL")
    social_links = models.JSONField(default=dict,blank=True,
        help_text='JSON object of social media URLs, e.g., {"facebook": "https://...", "instagram": "..."}')

    logo = models.ImageField(upload_to='business_logos/',
          validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],                    blank=True, null=True, help_text="Square logo (200x200px)")
    cover_image = models.ImageField(upload_to='business_covers/', blank=True, null=True, help_text="Banner image (1200x400px)")
    description = models.TextField(blank=True, help_text="Detailed description of business, services, history, etc.")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, help_text="Reason for rejection (if applicable)")
    is_featured = models.BooleanField(default=False, help_text="Is this a paid/promoted listing?")
    verified_badge = models.BooleanField(default=False, help_text="Blue checkmark — verified by admin")
    has_multiple_locations = models.BooleanField(default=False, help_text="Does this business operate from multiple branches?")
    primary_location = models.ForeignKey('BusinessLocation',on_delete=models.SET_NULL,
        null=True,blank=True,related_name='primary_for',help_text="Main/default location for display purposes")

    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="Custom title for search engines")
    meta_description = models.TextField(blank=True, null=True, help_text="Custom meta description for search engines")
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated keywords for SEO")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Business Listing"
        verbose_name_plural = "Business Listings"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while BusinessListing.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def display_status(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class BusinessLocation(models.Model):
    business = models.ForeignKey(BusinessListing, 
    on_delete=models.CASCADE, related_name="locations")
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    ward = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    latitude = models.CharField(max_length=9, null=True, blank=True)
    longitude = models.CharField(max_length=9, null=True, blank=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.business.name} - {self.municipality}"
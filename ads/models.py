from django.db import models
from django.utils import timezone
from listings.models import BusinessListing

class FeaturedListing(models.Model):
    business = models.OneToOneField(BusinessListing,on_delete=models.CASCADE,
                related_name='featured_promotion',help_text="Business is being promoted")
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(help_text="when promotion expires")
    is_active = models.BooleanField(default=True,help_text="Currently featured?")
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00,help_text="paid_amount")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-start_date']
        verbose_name = "Featured Listing"
        verbose_name_plural = "Featured Listings"

    def __str__(self):
        return f"Featured: {self.business.name} (until {self.end_date.strftime('%Y-%m-%d')})"

    @property
    def is_currently_active(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date
    

class BannerAd(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='ads/banners/', help_text="Recommended size: 728x90 or 300x250")
    url = models.URLField(help_text="where the banner links to")
    is_active = models.BooleanField(default=True, help_text="Show this banner?")
    position = models.CharField(
        max_length=50,
        choices=[
            ('homepage_top', 'Homepage Top'),
            ('homepage_bottom', 'Homepage Bottom'),
            ('category_top', 'Category Page Top'),
            ('category_bottom', 'Category Page Bottom'),
        ],
        default='homepage_top'
    )
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(help_text="When ad expires")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-start_date']
        verbose_name = "Banner Ad"
        verbose_name_plural = "Banner Ads"

    def __str__(self):
        return self.title
    


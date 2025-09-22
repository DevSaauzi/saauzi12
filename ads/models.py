from django.db import models
from django.utils import timezone
from listings.models import BusinessListing
from django.core.validators import MinValueValidator,MaxValueValidator
from userprofile.models import User



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
    



class Cupon(models.Model):
        STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
        ('used_up', 'Used Up'),
    ]
        business = models.ForeignKey(BusinessListing,on_delete=models.CASCADE,related_name="cupons")
        code = models.CharField(max_length=20,unique=True)
        discount_type = models.CharField( max_length=10,
        choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')],default='percentage')
        discount_value = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)],
            help_text="e.g., 10 for 10% off or Rs.10 off")   
        valid_form = models.DateTimeField()
        valid_until = models.DateTimeField()
        usage_limit = models.PositiveIntegerField(default=0,help_text="unlimited")
        used_count = models.PositiveBigIntegerField(default=0)
        status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
        rejection_reason = models.TextField(blank=True, null=True)
        is_active = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        class Meta:
             ordering =['-created_at']
             indexes = [
                  models.Index(fields=['business','status']),
                   models.Index(fields=['code']),
             ]

        def __str__(self):
             return f"{self.code}-{self.business.name}"
        
        
        def save(self, *args, **kwargs):
            now = timezone.now()
            self.is_active = (
                self.status == 'approved' and
                self.valid_from <= now <= self.valid_until and
                (self.usage_limit == 0 or self.used_count < self.usage_limit)
            )
            super().save(*args, **kwargs)



    
class Flashdeal(models.Model):
     STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('ended', 'Ended'),
    ]
     business = models.ForeignKey(BusinessListing,
                    on_delete=models.CASCADE,related_name="flashdeal")
     title = models.CharField(max_length=200)
     description = models.TextField()
     discount_percentage = models.PositiveIntegerField(validators=[MinValueValidator(1),
                            MaxValueValidator(99)],help_text="Discont_percentage(1-99%)") 
     starts_at = models.DateTimeField()
     ends_at = models.DateTimeField()
     max_redemptions = models.PositiveIntegerField(default=0, help_text="0 = unlimited")
     redemptions = models.PositiveIntegerField(default=0, editable=False)
     status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
     rejection_reason = models.TextField(blank=True, null=True)
     is_active = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
  
     class Meta:
        ordering = ['-starts_at']
        indexes = [
            models.Index(fields=['business', 'status']),
            models.Index(fields=['starts_at', 'ends_at']),
        ]

     def __str__(self):
        return f"{self.title} - {self.business.name}"

     def save(self, *args, **kwargs):
        now = timezone.now()
        self.is_active = (
            self.status == 'approved' and
            self.starts_at <= now <= self.ends_at and
            (self.max_redemptions == 0 or self.redemptions < self.max_redemptions)
        )
        super().save(*args, **kwargs)




class AdClick(models.Model):
    ad = models.ForeignKey(BannerAd, on_delete=models.CASCADE, related_name="clicks")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['ad', '-clicked_at']),
        ]

    def __str__(self):
        return f"Click on {self.ad.title} at {self.clicked_at}"        
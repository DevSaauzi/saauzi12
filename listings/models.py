from django.db import models
from userprofile.models import User
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=30,unique=True)
    slug = models.SlugField(max_length=50,unique=True,blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args,**kwargs)

  
class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="subcategories")
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=100,blank=True)
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
            return f"{self.name}"
        

    
    def __str__(self):
        cat_name = self.category.name if self.category else "Uncategorized"
        return f"{cat_name} → {self.name}"     


class BusinessListing(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('active','Active'),
        ('rejection','Rejection')
    ]
    owners = models.ForeignKey(User, on_delete=models.CASCADE,blank= True,null=True,related_name="business")
    name = models.CharField(max_length=100,help_text="Business_name")
    slug = models.SlugField(max_length=100,unique=True,blank=True)
    Category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name="listings")
    SubCategory = models.ForeignKey(SubCategory,on_delete=models.PROTECT,related_name="listings")
    phone = models.CharField(max_length=15,blank=True)
    email = models.EmailField(max_length=25,unique=True)
    website = models.URLField(blank=True)
    social_links = models.URLField(default=dict,blank=True)
    address_province = models.CharField(max_length=100, blank=True, null=True)
    address_district = models.CharField(max_length=100, blank=True, null=True)
    address_municipality = models.CharField(max_length=100, blank=True, null=True)
    address_ward = models.CharField(max_length=10, blank=True, null=True)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='business_covers/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, help_text="If rejected, why?")
    is_featured = models.BooleanField(default=False, help_text="Paid promotion")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
     
    class Meta:
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
    

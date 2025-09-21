from django.db import models
from listings.models import BusinessListing
class BusinessView(models.Model):
    business = models.ForeignKey(BusinessListing,on_delete=models.RESTRICT,related_name="views")
    ip_address = models.GenericIPAddressField(null= True,blank=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.business.name} viewed at {self.viewed_at}"   
    

class ContactClick(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('website', 'Website'),
    ]

    business = models.ForeignKey(BusinessListing, on_delete=models.CASCADE, related_name='contact_clicks')
    contact_type = models.CharField(max_length=10, choices=CONTACT_TYPE_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-clicked_at']

    def __str__(self):
        return f"{self.get_contact_type_display()} click for {self.business.name}"


class WeeklyRanking(models.Model):
    business = models.ForeignKey(BusinessListing,on_delete=models.CASCADE,related_name="weekely_ramking")
    week_start = models.DateField()
    view_count = models.PositiveBigIntegerField(default=0)
    click_count = models.PositiveBigIntegerField(default=0)
    ranking = models.PositiveBigIntegerField(help_text="1=most_popular")

    class Meta:
        ordering = ['week_start', 'ranking']

    def __str__(self):
      return f"{self.business.name}-{self.week_start}-{self.ranking}"
    
class MonthlyRanking(models.Model):
    business = models.ForeignKey(BusinessListing,on_delete=models.CASCADE,related_name="monthly_ranking")
    year = models.DateField()
    month_start = models.DateField()
    view_count = models.PositiveBigIntegerField(default=0)
    click_count = models.PositiveBigIntegerField(default=0)
    ranking = models.PositiveBigIntegerField(help_text="1=most_popular")

    class Meta:
       ordering = ['-year', '-month_start', 'ranking']  

    def __str__(self):
         return f"{self.bussiness.name}-{self.year}-{self.ranking}"  




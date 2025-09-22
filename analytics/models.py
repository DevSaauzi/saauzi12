from django.db import models
from listings.models import BusinessListing
from userprofile.models import User


# Business View

class BusinessView(models.Model):
    business = models.ForeignKey( BusinessListing,on_delete=models.CASCADE,related_name="views")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey( User, on_delete=models.CASCADE, null=True, blank=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.business.name} viewed at {self.viewed_at}"


# Contact Click

class ContactClick(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('website', 'Website'),
        ('whatsapp', 'WhatsApp'),
        ('directions', 'Directions'),
    ]

    business = models.ForeignKey(BusinessListing,on_delete=models.CASCADE,related_name='contact_clicks' )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    contact_type = models.CharField(max_length=15, choices=CONTACT_TYPE_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-clicked_at']

    def __str__(self):
        return f"{self.get_contact_type_display()} click for {self.business.name}"


# Weekly Ranking

class WeeklyRanking(models.Model):
    business = models.ForeignKey( BusinessListing,on_delete=models.CASCADE, related_name="weekly_rankings" )
    week_start = models.DateField()
    view_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ranking_score = models.FloatField(default=0.0, help_text="Computed score for sorting")
    ranking = models.PositiveIntegerField(null=True, blank=True, help_text="1=most_popular")
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['week_start', 'ranking']
        unique_together = ('business', 'week_start')
        indexes = [
            models.Index(fields=['week_start']),
            models.Index(fields=['-ranking_score']),
            models.Index(fields=['business', 'week_start']),
        ]

    def __str__(self):
        return f"{self.business.name} - Week {self.week_start}"  


# Monthly Ranking

class MonthlyRanking(models.Model):
    business = models.ForeignKey(
        BusinessListing,
        on_delete=models.CASCADE,
        related_name="monthly_rankings"
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    view_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ranking_score = models.FloatField(default=0.0, help_text="Computed score for sorting")
    ranking = models.PositiveIntegerField(null=True, blank=True, help_text="1=most_popular")
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-year', '-month', 'ranking']
        unique_together = ('business', 'year', 'month')
        indexes = [
            models.Index(fields=['-year', '-month']),
            models.Index(fields=['-ranking_score']),
            models.Index(fields=['business', '-year', '-month']),
        ]

    def __str__(self):
        return f"{self.business.name} - {self.year}/{self.month}"  
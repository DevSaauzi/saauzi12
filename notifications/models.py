

from django.db import models
from userprofile.models import User
from listings.models import BusinessListing
from businessreview.models import Review


class Notifications(models.Model):
    EVENT_TYPES = [
        ('listing_submitted', 'Listing Submitted'),
        ('listing_approved', 'Listing Approved'),
        ('listing_rejected', 'Listing Rejected'),
        ('new_review', 'New Review Posted'),
        ('review_reported', 'Review Reported'),
        ('promotion_approved', 'Promotion Approved'),
        ('coupon_redeemed', 'Coupon Redeemed'),
        ('location_added', 'New Location Added'),
        ('featured_listing_approved', 'Featured Listing Approved'),
        ('banner_ad_approved', 'Banner Ad Approved'),
        ('reply_to_review', 'Reply to Your Review'),
    ]

    DELIVERY_CHANNELS = [
        ('email', 'Email'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    related_business = models.ForeignKey(BusinessListing, on_delete=models.CASCADE, related_name="notifications")
    related_review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    related_promotion = models.CharField(max_length=100, blank=True, help_text="e.g., 'Coupon:SUMMER20' or 'FlashDeal:WeekendSale'")
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)
    delivery_channel = models.CharField(max_length=10, choices=DELIVERY_CHANNELS, default='in_app')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')

    class Meta:
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['recipient', 'read_status']),
            models.Index(fields=['event_type']),
            models.Index(fields=['-sent_at']),
        ]

    def __str__(self):
        return f"{self.event_type} for {self.recipient.username} at {self.sent_at}"

    def mark_as_read(self):
        self.read_status = True
        self.save(update_fields=['read_status'])


class NotificationsPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')  # ✅ Fixed related_name
    events_enabled = models.JSONField(default=list, help_text="List of event_type keys user wants to receive")
    delivery_channels = models.JSONField(default=list, help_text="e.g., ['email', 'push']")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prefs for {self.user.username}"

    @property
    def events_enabled_list(self):
        return ", ".join(self.events_enabled) if self.events_enabled else "None"

    @property
    def delivery_channels_list(self):
        return ", ".join(self.delivery_channels) if self.delivery_channels else "None"

    events_enabled_list.fget.short_description = "Enabled Events"
    delivery_channels_list.fget.short_description = "Delivery Channels"
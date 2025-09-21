

from django.db import models
from django.contrib.auth import get_user_model
from listings.models import BusinessListing
from businessreview.models import Review

User = get_user_model()

class NotificationLog(models.Model):

    EVENT_CHOICES = [
        ('listing_submitted', 'New Listing Submitted'),
        ('listing_approved', 'Listing Approved'),
        ('listing_rejected', 'Listing Rejected'),
        ('new_review', 'New Review Posted'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_received')
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    business = models.ForeignKey(BusinessListing, on_delete=models.CASCADE, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Notification Log"
        verbose_name_plural = "Notification Logs"

    def __str__(self):
        return f"{self.get_event_type_display()} → {self.recipient.email}"
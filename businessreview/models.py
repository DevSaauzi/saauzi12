from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from userprofile.models import User
from listings.models import BusinessListing


class Review(models.Model):
    business = models.ForeignKey(
        BusinessListing,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="The business being reviewed"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authored_reviews",
        limit_choices_to={'user_type__in': ['normal', 'owner']},
        help_text="Review written by the user"  
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('business', 'author')
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def save(self, *args, **kwargs):
        if self.author == self.business.owners:
            raise ValueError("Business owners are not allowed to review their own listing")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author.email} → {self.business.name} ({self.rating}★)"

    @property
    def is_reported(self):
        return self.reports.exists()  


class ReportedReview(models.Model):
    reviewed = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="reports",
        help_text="The review being reported"
    )
    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="review_reports",
        help_text="User who reported the review"
    )
    reason = models.TextField(blank=True, help_text="Reason for the report")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Reported Review"
        verbose_name_plural = "Reported Reviews"

    def __str__(self):
        return f"Review #{self.reviewed.id} reported by {self.reported_by.email}" 

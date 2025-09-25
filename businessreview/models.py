from django.db import models
from django.core.exceptions import ValidationError
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
    rating = models.DecimalField(max_digits=3,decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Overall rating from 1 to 5"
    )

    comment = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False, help_text="True if user actually used the service")
    media = models.FileField(upload_to='reviews/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('business', 'author')
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        indexes = [
            models.Index(fields=['business', '-created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['rating']),
        ]

    def clean(self):
        if self.author == self.business.owner:
            raise ValidationError("Business owners cannot review their own business.")
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.author.email} → {self.business.name} ({self.rating}★)"

    @property
    def is_reported(self):
        return self.reports.exists()

    @property
    def weighted_rating(self):
        sub_ratings = [
            self.rating_quality,
            self.rating_price,
            self.rating_service,
            self.rating_cleanliness,
        ]
        valid_ratings = [r for r in sub_ratings if r is not None]
        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return float(self.rating)


class ReportedReview(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]

    reviewed = models.ForeignKey(Review,on_delete=models.CASCADE,related_name="reports",
        help_text="The review being reported")
    reported_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="review_reports",
        help_text="User who reported the review")
    reason = models.TextField(blank=True, help_text="Reason for the report")
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending',
                              help_text="Admin review status")
    resolved_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,
        limit_choices_to={'user_type': 'admin'},related_name="resolved_reports",
        help_text="Admin who resolved this report")
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Reported Review"
        verbose_name_plural = "Reported Reviews"

    def clean(self):
        if self.reported_by == self.reviewed.author:
            raise ValidationError("You cannot report your own review.")
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review #{self.reviewed.id} reported by {self.reported_by.email}"


class ReviewReply(models.Model):
    review = models.OneToOneField(Review,on_delete=models.CASCADE,related_name="reply",
        help_text="The review being replied to")
    owner = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'user_type': 'owner'},
        help_text="Must be the business owner")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Review Reply"
        verbose_name_plural = "Review Replies"

    def clean(self):
        if self.owner != self.review.business.owner:
            raise ValidationError("Only the business owner can reply to this review.")
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reply by {self.owner.email} to review #{self.review.id}"
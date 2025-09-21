from django.contrib import admin
from .models import Review, ReportedReview


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['business', 'author', 'rating', 'is_reported', 'created_at']
    list_filter = ['rating', 'created_at', 'business__Category']  
    search_fields = ['author__email', 'business__name', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['mark_as_unreported']

    @admin.action(description="Mark selected reviews as NOT reported")
    def mark_as_unreported(self, request, queryset):
        ReportedReview.objects.filter(reviewed__in=queryset).delete()
        self.message_user(request, f"Reports cleared for {queryset.count()} reviews.")


@admin.register(ReportedReview)
class ReportedReviewAdmin(admin.ModelAdmin):  
    list_display = ['reviewed', 'reported_by', 'created_at', 'reason']  
    list_filter = ['reported_by', 'created_at']
    search_fields = ['reported_by__email', 'reviewed__business__name']
    readonly_fields = ['created_at']
  
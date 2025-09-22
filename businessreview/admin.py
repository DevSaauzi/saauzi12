from django.contrib import admin
from .models import Review, ReportedReview,ReviewReply


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['business', 'author', 'rating', 'is_reported', 'created_at']
    list_filter = ['rating', 'created_at', ]  
    search_fields = ['author__email', 'business__name', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    

  


@admin.register(ReportedReview)
class ReportedReviewAdmin(admin.ModelAdmin):  
    list_display = ['reviewed', 'reported_by', 'created_at', 'reason']  
    list_filter = ['reported_by', 'created_at']
    search_fields = ['reported_by__email', 'reviewed__business__name']
    readonly_fields = ['created_at']
  


@admin.register(ReviewReply)
class ReviewReplyAdmin(admin.ModelAdmin):
    list_display = ['review__business', 'owner', 'created_at', 'updated_at']
    list_filter = ['owner', 'created_at']
    search_fields = ['owner__email','owner__username','review__business__name','message']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['review', 'owner']  
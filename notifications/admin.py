from django.contrib import admin
from .models import NotificationLog


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = [
        'recipient',           
        'event_type',          
        'business',            
        'review',            
        'sent_at',
    ]
    list_filter = [
        'event_type',
        'sent_at',
        'recipient',
    ]
    search_fields = [
        'recipient__email',
        'recipient__username',
        'business__name',
        'subject',
        'message',
    ]
    readonly_fields = [
        'recipient',
        'event_type',
        'business',
        'review',
        'sent_at',
        'subject',
        'message',
    ]

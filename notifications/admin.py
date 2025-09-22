
from django.contrib import admin
from .models import Notifications, NotificationsPreference


@admin.register(Notifications)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['recipient','event_type','related_business','related_review','sent_at',]
    list_filter = ['event_type', 'sent_at', 'recipient']
    search_fields = ['recipient__email','recipient__username','related_business__name','subject','message',]
    readonly_fields = ['recipient','event_type','related_business','related_review','sent_at',
                      'subject','message','delivery_channel','priority','read_status',]
    date_hierarchy = 'sent_at'


@admin.register(NotificationsPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user','events_enabled_list','delivery_channels_list','updated_at',]
    list_filter = ['updated_at']   
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['updated_at', 'events_enabled_list', 'delivery_channels_list']

 
    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        if obj:  
            fields += ['user', 'events_enabled', 'delivery_channels']
        return fields
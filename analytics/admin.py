from django.contrib import admin
from analytics.models import BusinessView,ContactClick,WeeklyRanking,MonthlyRanking

@admin.register(BusinessView)
class BusinessViewAdmin(admin.ModelAdmin):
    list_display = ['business', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['business__name']
    autocomplete_fields = ['business']
    date_hierarchy = 'viewed_at'
    ordering = ['-viewed_at']


@admin.register(ContactClick)
class ContactClickAdmin(admin.ModelAdmin):
    list_display = ['business', 'contact_type', 'clicked_at']
    list_filter = ['contact_type', 'clicked_at']
    search_fields = ['business__name']
    autocomplete_fields = ['business']




@admin.register(WeeklyRanking)
class WeeklyRankingAdmin(admin.ModelAdmin):
    list_display = ['business', 'week_start', 'view_count', 'click_count', 'ranking']
    list_filter = ['business', 'ranking', 'week_start']
    search_fields = ['business__name']
    autocomplete_fields = ['business']
    date_hierarchy = 'week_start'
    ordering = ['-week_start', 'ranking']


@admin.register(MonthlyRanking)
class MonthlyRankingAdmin(admin.ModelAdmin):
    list_display = ['business', 'year', 'month', 'view_count', 'click_count', 'ranking']
    list_filter = ['business', 'ranking', 'year']
    search_fields = ['business__name']
    autocomplete_fields = ['business']



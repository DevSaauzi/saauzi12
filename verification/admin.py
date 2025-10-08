from django.contrib import admin
from .models import Verification

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ['business', 'is_fully_verified',]
    readonly_fields = [
        'email_otp',
        'email_otp_created_at',
       
    ]
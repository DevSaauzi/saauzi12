import re
import secrets
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone  
from listings.models import BusinessListing


class Verification(models.Model):
    business = models.OneToOneField(
        BusinessListing,
        on_delete=models.CASCADE,
        related_name="verification"
    )

    pan_card = models.FileField(
        upload_to='verification/pan/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])],
        blank=True,
        null=True,
        help_text="Upload PAN card for verification"
    )
    citizenship = models.FileField(
        upload_to='verification/citizenship/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf'])],
        blank=True,
        null=True,
        help_text="Upload your citizenship certificate"
    )

    # Document data
    pan_number = models.CharField(max_length=25, blank=True, help_text="PAN number from your PAN card")
    citizenship_number = models.CharField(max_length=25, blank=True, help_text="Citizenship ID number")
    owner_name = models.CharField(max_length=100, blank=True, help_text="Owner name as per official documents")

    # Meta tags
    has_valid_metatags = models.BooleanField(default=False, help_text="Auto-checked or manually confirmed")
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True, default="")

    # Email & OTP
    is_email_domain_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, blank=True)
    email_otp_created_at = models.DateTimeField(null=True, blank=True,default=None)
    email_otp_attempts = models.PositiveSmallIntegerField(default=0)

    # Status flags
    is_pan_verified = models.BooleanField(default=False)
    is_citizenship_verified = models.BooleanField(default=False)
    is_fully_verified = models.BooleanField(default=False)

    
    class Meta:
        verbose_name = "Business Verification"
        verbose_name_plural = "Business Verifications"

    def __str__(self):
        status = "Verified" if self.is_fully_verified else "Pending"
        return f"Verification for {self.business.name} – {status}"



    def validate_pan(self):
        if not self.pan_number:
            return False, "PAN number is missing."

        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', self.pan_number.upper()):
            return False, "Invalid PAN format."

        owner_name = ""
        if self.business.owner and hasattr(self.business.owner, 'full_name'):
            owner_name = self.business.owner.full_name.strip().upper()

        doc_name = self.owner_name.strip().upper()

        if owner_name and doc_name and owner_name != doc_name:
            return False, f"Name mismatch: '{doc_name}' ≠ '{owner_name}'"

        return True, "PAN verified."

    def validate_citizenship(self):
        if not self.citizenship_number:
            return False, "Citizenship number is missing."

        if not self.citizenship_number.isdigit():
            return False, "Citizenship ID must be numeric."

        owner_name = ""
        if self.business.owner and hasattr(self.business.owner, 'full_name'):
            owner_name = self.business.owner.full_name.strip().upper()

        doc_name = self.owner_name.strip().upper()

        if owner_name and doc_name and owner_name != doc_name:
            return False, f"Name mismatch: '{doc_name}' ≠ '{owner_name}'"

        return True, "Citizenship verified."

    def validate_meta_tags(self):
        title = self.meta_title or self.business.meta_title
        desc = self.meta_description or self.business.meta_description

        if not title or not desc:
            return False, "Meta title and description are required."

        if len(desc) < 50:
            return False, "Meta description is too short (minimum 50 characters)."

        return True, "Meta tags are valid."

    def validate_email_domain(self):
        email = self.business.email
        if not email:
            return False, "Business email is required."

        domain = email.split('@')[-1].lower()
        free_domains = {'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com'}

        if domain in free_domains:
            return False, f"Use your business domain (e.g., contact@{self.business.name.replace(' ', '').lower()}.com), not {domain}."

        try:
            import dns.resolver
            dns.resolver.resolve(domain, 'MX')
        except Exception:
            return False, f"Domain {domain} has no email support (no MX record)."

        return True, f"Domain {domain} is valid."

    

    def generate_email_otp(self):
        self.email_otp = str(secrets.randbelow(1000000)).zfill(6)
        self.email_otp_created_at = timezone.now()  
        self.email_otp_attempts = 0
        self.save(update_fields=['email_otp', 'email_otp_created_at', 'email_otp_attempts'])

    def verify_email_otp(self, otp: str) -> bool:
        from datetime import timedelta

        if self.email_otp_attempts >= 3:
            return False

        if not self.email_otp or otp != self.email_otp:
            self.email_otp_attempts += 1
            self.save(update_fields=['email_otp_attempts'])
            return False

        if self.email_otp_created_at:
            if (timezone.now() - self.email_otp_created_at) > timedelta(minutes=10):
                return False
        self.is_email_domain_verified = True
        self.email_otp = ""  
        self.save(update_fields=['is_email_domain_verified', 'email_otp'])
        return True


    def run_verification(self):
        pan_ok, _ = self.validate_pan()
        cit_ok, _ = self.validate_citizenship()
        meta_ok, _ = self.validate_meta_tags()

        self.is_pan_verified = pan_ok
        self.is_citizenship_verified = cit_ok
        self.has_valid_metatags = meta_ok
        self.is_fully_verified = pan_ok and cit_ok and self.is_email_domain_verified

        self.save(update_fields=[
            'is_pan_verified',
            'is_citizenship_verified',
            'has_valid_metatags',
            'is_fully_verified'
        ])
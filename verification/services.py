from django.core.mail import send_mail
from django.conf import settings
from .models import Verification


def run_initial_verification(verification: Verification):
    verification.run_verification()


def send_email_otp(verification: Verification):
    domain_ok, message = verification.validate_email_domain()
    if not domain_ok:
        raise ValueError(message)

    verification.generate_email_otp()
    send_mail(
        subject="Verify Your Business Email – Find Your Saauzi",
        message=f"Your OTP is: {verification.email_otp}\nValid for 10 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[verification.business.email],
        fail_silently=False,
    )


def verify_email_otp(verification: Verification, otp: str) -> bool:
    return verification.verify_email_otp(otp)
import secrets
from datetime import timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from .models import OTPVerification


OTP_EXPIRY_MINUTES = 1
RESEND_COOLDOWN_MINUTES = 1
MAX_OTP_ATTEMPTS = 5


def generate_otp():
    """
    Generate a secure 6-digit OTP.
    """
    return f"{secrets.randbelow(1_000_000):06d}"


def create_otp(user):
    """
    Create a new OTP for a user.
    The OTP expires after 1 minute.
    A new OTP can only be requested after 1 minute.
    """

    now = timezone.now()

    # Find the most recently created OTP
    recent_otp = OTPVerification.objects.filter(
        user=user
    ).order_by("-created_at").first()

    # Enforce 1-minute resend cooldown
    if recent_otp:
        cooldown_time = recent_otp.created_at + timedelta(
            minutes=RESEND_COOLDOWN_MINUTES
        )

        if now < cooldown_time:
            raise ValueError(
                "Please wait 1 minute before requesting another OTP."
            )

    # Invalidate any previous unused OTPs
    OTPVerification.objects.filter(
        user=user,
        is_used=False
    ).update(
        is_used=True
    )

    # Generate a new OTP
    otp = generate_otp()

    # Hash the OTP before storing it
    hashed_otp = make_password(otp)

    # Store the new OTP
    OTPVerification.objects.create(
        user=user,
        otp_hash=hashed_otp,
        expires_at=now + timedelta(minutes=OTP_EXPIRY_MINUTES),
        is_used=False,
        attempts=0
    )

    return otp


def verify_otp(user, otp):
    """
    Verify a user's OTP.
    """

    verification = OTPVerification.objects.filter(
        user=user,
        is_used=False
    ).order_by("-created_at").first()

    if not verification:
        return False, "No valid OTP found."

    # Check expiration
    if timezone.now() >= verification.expires_at:
        verification.is_used = True
        verification.save(update_fields=["is_used"])

        return False, "OTP has expired."

    # Check maximum attempts
    if verification.attempts >= MAX_OTP_ATTEMPTS:
        verification.is_used = True
        verification.save(update_fields=["is_used"])

        return False, "Too many incorrect attempts."

    # Check OTP
    if not check_password(otp, verification.otp_hash):

        verification.attempts += 1
        verification.save(update_fields=["attempts"])

        remaining = MAX_OTP_ATTEMPTS - verification.attempts

        return False, f"Invalid OTP. {remaining} attempts remaining."

    # OTP is correct
    verification.is_used = True
    verification.save(update_fields=["is_used"])

    # Verify user's phone number
    user.phone_verified = True
    user.save(update_fields=["phone_verified"])

    return True, "Phone number verified successfully."
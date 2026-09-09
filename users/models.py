from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('ARTISAN', 'Artisan/Worker'),
    )

    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='CUSTOMER'
    )

    email = models.EmailField(
        unique=True
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )

    phone_verified = models.BooleanField(
        default=False
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username


class OTPVerification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='otp_verifications'
    )

    otp_hash = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(
        default=False
    )

    attempts = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"OTP for {self.user.username}"
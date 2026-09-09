from django.conf import settings
from django.db import models


class ProviderProfile(models.Model):

    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='provider_profile'
    )

    profession = models.CharField(
        max_length=100,
        help_text="e.g. Electrician, Plumber, Carpenter"
    )

    years_of_experience = models.PositiveIntegerField(
        default=0,
        help_text="Years of professional experience"
    )

    state = models.CharField(
        max_length=100
    )

    city_lga = models.CharField(
        max_length=100,
        verbose_name="City or LGA"
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    is_verified = models.BooleanField(
        default=False
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.profession}"
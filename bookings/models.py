from django.conf import settings
from django.db import models
from providers.models import ProviderProfile
from services.models import Service


class Booking(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_bookings'
    )

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='provider_bookings'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )

    booking_date = models.DateField()
    booking_time = models.TimeField()
    service_address = models.TextField()
    additional_notes = models.TextField(null=True, blank=True)

    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    booking_fee = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.service_fee + self.booking_fee
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking #{self.id} - {self.customer.username} with {self.provider.user.username}"
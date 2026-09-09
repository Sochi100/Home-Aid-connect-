from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Booking
from .serializers import BookingSerializer


@extend_schema(tags=["Bookings"])
class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ARTISAN':
            return Booking.objects.filter(provider__user=user)
        return Booking.objects.filter(customer=user)


@extend_schema(tags=["Bookings"])
class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ARTISAN':
            return Booking.objects.filter(provider__user=user)
        return Booking.objects.filter(customer=user)
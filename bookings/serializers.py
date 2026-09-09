from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    provider_name = serializers.CharField(source='provider.user.get_full_name', read_only=True)
    provider_profession = serializers.CharField(source='provider.profession', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'customer',
            'customer_name',
            'provider',
            'provider_name',
            'provider_profession',
            'service',
            'booking_date',
            'booking_time',
            'service_address',
            'additional_notes',
            'service_fee',
            'booking_fee',
            'total_amount',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'customer', 'total_amount', 'status', 'created_at']

    def create(self, validated_data):
        # Automatically assign logged-in user as the customer
        request = self.context.get('request')
        validated_data['customer'] = request.user
        return super().create(validated_data)
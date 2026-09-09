from rest_framework import serializers
from .models import EmergencyAlert


class EmergencyAlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmergencyAlert
        fields = [
            'id',
            'user',
            'latitude',
            'longitude',
            'location_address',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
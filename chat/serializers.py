from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'sender_name',
            'recipient',
            'recipient_name',
            'text',
            'is_read',
            'created_at',
        ]
        read_only_fields = ['id', 'sender', 'is_read', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['sender'] = request.user
        return super().create(validated_data)
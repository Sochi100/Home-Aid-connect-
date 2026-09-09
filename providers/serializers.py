from rest_framework import serializers
from .models import ProviderProfile


class ProviderProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = ProviderProfile
        fields = [
            'id',
            'user',
            'username',
            'full_name',
            'profession',
            'years_of_experience',
            'state',
            'city_lga',
            'gender',
            'is_verified',
            'rating',
        ]
        read_only_fields = ['id', 'user', 'is_verified', 'rating']
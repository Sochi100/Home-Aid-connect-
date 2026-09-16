from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .otp import create_otp

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        max_length=20
    )

    password_confirm = serializers.CharField(
        write_only=True,
        max_length=20
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "phone_number",
            "role",
            "gender",
            "location",
            "date_of_birth",
        ]

    def validate_email(self, value):
        value = value.lower()

        if not value.endswith(
            (".com", ".org", ".net", ".ng", ".co")
        ):
            raise serializers.ValidationError(
                "Please enter a valid email address."
            )

        return value

    def validate_phone_number(self, value):
        if not value.startswith("+234"):
            raise serializers.ValidationError(
                "Phone number must start with +234."
            )

        if len(value) != 14:
            raise serializers.ValidationError(
                "Enter a valid Nigerian phone number."
            )

        if not value[1:].isdigit():
            raise serializers.ValidationError(
                "Phone number must contain numbers only."
            )

        return value

    def validate(self, attrs):

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })

        return attrs

    def create(self, validated_data):

        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(
        min_length=6,
        max_length=6
    )

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "OTP must contain numbers only."
            )

        return value


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        max_length=20
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        u_usernname = User.objects.filter(email=email).first()
        u_user = u_usernname.username if u_usernname else None

        user = authenticate(
            username=u_user,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid email address or password."
            )

        if hasattr(user, 'phone_verified') and not user.phone_verified:
            raise serializers.ValidationError(
                "Please verify your email address before logging in."
            )

        attrs["user"] = user

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'gender',
            'date_of_birth',
            'location',
            'role',
            'phone_verified',
        ]
        read_only_fields = ['id', 'username', 'role', 'phone_verified']
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from .otp import verify_otp, create_otp
from .utils import send_termii_otp  # Import Termii helper function

from .serializers import (
    RegisterSerializer,
    VerifyOTPSerializer,
    ResendOTPSerializer,
    LoginSerializer,
    UserProfileSerializer
)


User = get_user_model()


# ============================================================
# REGISTER
# ============================================================

@extend_schema(
    request=RegisterSerializer,
    auth=[],
    tags=["Authentication"]
)
class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        # Generate OTP and send via Termii SMS
        try:
            otp = create_otp(user)
            send_termii_otp(user.phone_number, otp)
        except Exception as error:
            print(f"OTP Generation / Termii Error: {error}")

        return Response(
            {
                "success": True,
                "message": (
                    "Registration successful. "
                    "OTP sent to your phone."
                ),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_number,
                    "gender": user.gender,
                    "date_of_birth": user.date_of_birth,
                    "location": user.location,
                    "role": user.role
                }
            },
            status=status.HTTP_201_CREATED
        )


# ============================================================
# VERIFY OTP
# ============================================================

@extend_schema(
    request=VerifyOTPSerializer,
    auth=[],
    tags=["Authentication"]
)
class VerifyOTPView(APIView):

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        phone_number = serializer.validated_data[
            "phone_number"
        ]

        otp = serializer.validated_data[
            "otp"
        ]

        try:

            user = User.objects.get(
                phone_number=phone_number
            )

        except User.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "No user found with this "
                        "phone number."
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        success, message = verify_otp(
            user,
            otp
        )

        if not success:

            return Response(
                {
                    "success": False,
                    "message": message
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": message
            },
            status=status.HTTP_200_OK
        )


# ============================================================
# RESEND OTP
# ============================================================

@extend_schema(
    request=ResendOTPSerializer,
    auth=[],
    tags=["Authentication"]
)
class ResendOTPView(APIView):

    def post(self, request):

        serializer = ResendOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        phone_number = serializer.validated_data[
            "phone_number"
        ]

        try:

            user = User.objects.get(
                phone_number=phone_number
            )

        except User.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "No user found with this "
                        "phone number."
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if user.phone_verified:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Phone number is already "
                        "verified."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            otp = create_otp(user)
            send_termii_otp(user.phone_number, otp)

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        return Response(
            {
                "success": True,
                "message": (
                    "A new OTP has been sent to your phone."
                )
            },
            status=status.HTTP_200_OK
        )


# ============================================================
# LOGIN
# ============================================================

@extend_schema(
    request=LoginSerializer,
    auth=[],
    tags=["Authentication"]
)
class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data[
            "user"
        ]

        refresh = RefreshToken.for_user(
            user
        )

        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_number,
                    "gender": user.gender,
                    "date_of_birth": user.date_of_birth,
                    "location": user.location,
                    "role": user.role
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(
                        refresh.access_token
                    )
                }
            },
            status=status.HTTP_200_OK
        )


# ============================================================
# USER PROFILE
# ============================================================

@extend_schema(
    responses=UserProfileSerializer,
    tags=["User Profile"]
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
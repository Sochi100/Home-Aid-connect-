from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .otp import verify_otp, create_otp

from .serializers import (
    RegisterSerializer,
    VerifyOTPSerializer,
    ResendOTPSerializer,
    LoginSerializer,
    UserProfileSerializer
)

User = get_user_model()


# Helper function to dispatch OTP via Django SMTP
def send_otp_email(user_email, otp_code):
    subject = "Your HomeAid Connect Verification Code"
    message = f"Hello,\n\nYour verification code is: {otp_code}\n\nThis code will expire shortly."
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )


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

        # Generate OTP and send via Email (SMTP)
        try:
            otp = create_otp(user)
            send_otp_email(user.email, otp)
        except Exception as error:
            print(f"OTP Generation / Email Error: {error}")

        return Response(
            {
                "success": True,
                "message": (
                    "Registration successful. "
                    "OTP sent to your email address."
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

        email = serializer.validated_data[
            "email"
        ]

        otp = serializer.validated_data[
            "otp"
        ]

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "No user found with this "
                        "email address."
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

        email = serializer.validated_data[
            "email"
        ]

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "No user found with this "
                        "email address."
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if getattr(user, 'phone_verified', False):

            return Response(
                {
                    "success": False,
                    "message": (
                        "Account is already verified."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            otp = create_otp(user)
            send_otp_email(user.email, otp)

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
                    "A new OTP has been sent to your email."
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
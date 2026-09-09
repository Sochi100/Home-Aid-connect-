from django.urls import path

from .views import (
    RegisterView,
    VerifyOTPView,
    ResendOTPView,
    LoginView,
    UserProfileView
)


urlpatterns = [

    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "verify-otp/",
        VerifyOTPView.as_view(),
        name="verify-otp"
    ),

    path(
        "resend-otp/",
        ResendOTPView.as_view(),
        name="resend-otp"
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "me/",
        UserProfileView.as_view(),
        name="user-profile"
    ),

]
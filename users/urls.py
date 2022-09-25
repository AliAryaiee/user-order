from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views


urlpatterns = [
    path("register", views.UserRegister.as_view()),
    path("profile", views.UserProfile.as_view()),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    # path("logout", knox.LogoutView.as_view()),
    # path("logoutall", knox.LogoutAllView.as_view()),
    # path("change-pass", views.UserChangePassword.as_view()),
    # path("send-otp", views.SendOTP.as_view()),
    # path("validate-otp", views.ConfirmOTP.as_view()),
    # path("tokens", views.UserTokens.as_view()),
]

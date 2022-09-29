from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views


urlpatterns = [
    path("register", views.UserRegister.as_view(), name="register-user"),
    path("profile", views.UserProfile.as_view(), name="user-profile"),
    path('token', TokenObtainPairView.as_view(), name="get-token"),
    path('token/refresh', TokenRefreshView.as_view(), name="refresh-token"),
]

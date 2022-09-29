from django.urls import path

from . import views


urlpatterns = [
    path("register", views.OrderView.as_view(), name="register-order"),
    path("all", views.UserOrders.as_view(), name="orders-list"),
]

from django.urls import path

from . import views


urlpatterns = [
    path("register", views.OrderView.as_view()),
    path("all", views.UserOrders.as_view()),
]

"""Корневые маршруты проекта."""

from django.urls import include, path

from booking import views

urlpatterns = [
    path("", views.home, name="home"),
    path("bookings/", include("booking.urls")),
]

handler404 = "booking.views.not_found"

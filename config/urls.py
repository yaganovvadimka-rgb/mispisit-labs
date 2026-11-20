"""Корневые маршруты проекта."""

from django.urls import include, path

from booking import views

urlpatterns = [
    path("", views.home, name="home"),
    path("bookings/", include("booking.urls")),
    path("notifications/", views.notification_list, name="notification_list"),
    path("notifications/<int:notification_id>/read/", views.notification_read,
         name="notification_read"),
]

handler404 = "booking.views.not_found"

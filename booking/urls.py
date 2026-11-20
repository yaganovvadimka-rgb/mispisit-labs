"""Маршруты раздела «Записи на обслуживание»."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.booking_list, name="booking_list"),
    path("new/", views.booking_create, name="booking_create"),
    path("rejected/", views.booking_rejected, name="booking_rejected"),
    path("<int:booking_id>/", views.booking_detail, name="booking_detail"),
]

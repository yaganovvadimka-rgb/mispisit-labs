"""Общие данные для всех страниц."""

from django.conf import settings

from .models import Notification


def app_info(request):
    return {
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
        "unread_notifications_count": Notification.objects.filter(
            status=Notification.STATUS_NEW,
        ).count(),
    }

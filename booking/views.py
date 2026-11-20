"""Обработчики трёх главных функций: создать запись, посмотреть записи, отказ."""

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import Booking, Master, Rejection, Service
from .rules import check_booking


def home(request):
    context = {
        "bookings_count": Booking.objects.count(),
        "rejections_count": Rejection.objects.count(),
        "services": Service.objects.all(),
    }
    return render(request, "index.html", context)


def booking_list(request):
    bookings = Booking.objects.select_related("service", "master")
    return render(request, "bookings/list.html", {"bookings": bookings})


def booking_detail(request, booking_id):
    b = get_object_or_404(Booking.objects.select_related("service", "master"), pk=booking_id)
    return render(request, "bookings/detail.html", {"b": b})


def _reject(post, reason):
    """Записать отказ в журнал и вернуть его номер."""

    def name(model, key):
        try:
            return model.objects.get(pk=int(post.get(key))).name
        except (TypeError, ValueError, model.DoesNotExist):
            return "не указано"

    rejection = Rejection.objects.create(
        client_name=post.get("client_name", "").strip()[:100] or "не указано",
        service_name=name(Service, "service"),
        master_name=name(Master, "master"),
        requested=(f'{post.get("date") or "дата не указана"} '
                   f'{post.get("time") or "время не указано"}')[:40],
        reason=reason,
    )
    return rejection.id


def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if not form.is_valid():
            reason = "; ".join(
                f"{form.fields[f].label}: {', '.join(e.rstrip('.') for e in errs).lower()}"
                if f in form.fields else ", ".join(errs)
                for f, errs in form.errors.items()
            )
            rid = _reject(request.POST, "Форма заполнена неверно. " + reason + ".")
            return redirect(f"/bookings/rejected/?id={rid}")

        data = form.cleaned_data
        with transaction.atomic():
            # Блокируем строку мастера, чтобы две одновременные записи не заняли одно время.
            Master.objects.select_for_update().get(pk=data["master"].pk)
            reason = check_booking(data)
            if not reason:
                booking = Booking.objects.create(
                    client_name=data["client_name"],
                    phone=data["phone"],
                    car=data["car"],
                    plate=data["plate"],
                    service=data["service"],
                    master=data["master"],
                    date=data["date"],
                    time=data["time"],
                    comment=data["comment"],
                )
        if reason:
            rid = _reject(request.POST, reason)
            return redirect(f"/bookings/rejected/?id={rid}")
        return redirect(f"/bookings/{booking.id}/?created=1")

    return render(request, "bookings/form.html", {"form": BookingForm()})


def booking_rejected(request):
    rejections = Rejection.objects.all()
    current = None
    try:
        current = rejections.filter(pk=int(request.GET.get("id", ""))).first()
    except ValueError:
        pass
    if current is None:
        current = rejections.first()
    return render(request, "bookings/rejected.html",
                  {"current": current, "rejections": rejections})


def not_found(request, exception=None):
    return render(request, "404.html", status=404)

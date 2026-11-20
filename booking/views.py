"""Обработчики трёх главных функций: создать запись, посмотреть записи, отказ."""

from datetime import datetime

from django.http import Http404
from django.shortcuts import redirect, render

from . import storage
from .forms import BookingForm
from .rules import booking_interval, check_booking


def _enrich(booking):
    """Добавить к записи названия услуги и мастера, время окончания."""
    service = storage.services()[booking["service_id"]]
    master = storage.masters()[booking["master_id"]]
    start, end = booking_interval(booking["date"], booking["time"], service["duration_min"])
    return {**booking, "service": service, "master": master, "start": start, "end": end}


def home(request):
    bookings = storage.load("bookings")
    context = {
        "bookings_count": len(bookings),
        "rejections_count": len(storage.load("rejections")),
        "services": storage.load("services"),
    }
    return render(request, "index.html", context)


def booking_list(request):
    bookings = sorted((_enrich(b) for b in storage.load("bookings")),
                      key=lambda b: b["start"])
    return render(request, "bookings/list.html", {"bookings": bookings})


def booking_detail(request, booking_id):
    for b in storage.load("bookings"):
        if b["id"] == booking_id:
            return render(request, "bookings/detail.html", {"b": _enrich(b)})
    raise Http404("Запись не найдена")


def _reject(post, reason):
    """Записать отказ в журнал и вернуть его номер."""
    services = storage.services()
    masters = storage.masters()

    def name(table, key):
        try:
            return table[int(post.get(key))]["name"]
        except (TypeError, ValueError, KeyError):
            return "не указано"

    item = storage.append("rejections", {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "client_name": post.get("client_name", "").strip() or "не указано",
        "action": "Запись на обслуживание",
        "service": name(services, "service"),
        "master": name(masters, "master"),
        "requested": f'{post.get("date") or "дата не указана"} '
                     f'{post.get("time") or "время не указано"}',
        "reason": reason,
    })
    return item["id"]


def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if not form.is_valid():
            reason = "; ".join(
                f"{form.fields[f].label}: {', '.join(e.rstrip('.') for e in errs).lower()}" if f in form.fields
                else ", ".join(errs)
                for f, errs in form.errors.items()
            )
            rid = _reject(request.POST, "Форма заполнена неверно. " + reason + ".")
            return redirect(f"/bookings/rejected/?id={rid}")

        data = form.cleaned_data
        reason = check_booking(data)
        if reason:
            rid = _reject(request.POST, reason)
            return redirect(f"/bookings/rejected/?id={rid}")

        booking = storage.append("bookings", {
            "client_name": data["client_name"],
            "phone": data["phone"],
            "car": data["car"],
            "plate": data["plate"],
            "service_id": data["service"],
            "master_id": data["master"],
            "date": data["date"].isoformat(),
            "time": data["time"].strftime("%H:%M"),
            "comment": data["comment"],
            "status": "Новая",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        return redirect(f"/bookings/{booking['id']}/?created=1")

    return render(request, "bookings/form.html", {"form": BookingForm()})


def booking_rejected(request):
    rejections = sorted(storage.load("rejections"), key=lambda r: r["id"], reverse=True)
    try:
        current_id = int(request.GET.get("id", ""))
    except ValueError:
        current_id = None
    current = next((r for r in rejections if r["id"] == current_id), None)
    if current is None and rejections:
        current = rejections[0]
    return render(request, "bookings/rejected.html",
                  {"current": current, "rejections": rejections})


def not_found(request, exception=None):
    return render(request, "404.html", status=404)

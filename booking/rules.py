"""Бизнес-правила записи: рабочее время, запрет записи в прошлое и пересечений."""

from datetime import datetime, time, timedelta

from . import storage

WORK_START = time(9, 0)
WORK_END = time(19, 0)


def booking_interval(date_str, time_str, duration_min):
    start = datetime.fromisoformat(f"{date_str}T{time_str}")
    return start, start + timedelta(minutes=duration_min)


def check_booking(data):
    """Вернуть текст причины отказа или None, если запись допустима."""
    service = storage.services()[data["service"]]
    master = storage.masters()[data["master"]]
    start = datetime.combine(data["date"], data["time"])
    end = start + timedelta(minutes=service["duration_min"])

    if start < datetime.now():
        return "Нельзя записаться на прошедшую дату или время."

    if start.time() < WORK_START or end.time() > WORK_END or end.date() != start.date():
        return (f"Автосервис работает с {WORK_START:%H:%M} до {WORK_END:%H:%M}. "
                f"Услуга «{service['name']}» длится {service['duration_min']} мин "
                f"и не помещается в рабочий день при начале в {start:%H:%M}.")

    if service["id"] not in master["service_ids"]:
        return (f"Мастер {master['name']} не выполняет услугу «{service['name']}». "
                f"Его специализация: {master['specialization']}.")

    services = storage.services()
    for b in storage.load("bookings"):
        if b["master_id"] != master["id"] or b["status"] == "Отменена":
            continue
        b_start, b_end = booking_interval(
            b["date"], b["time"], services[b["service_id"]]["duration_min"])
        if start < b_end and b_start < end:
            return (f"Мастер {master['name']} занят с {b_start:%H:%M} до {b_end:%H:%M} "
                    f"{b_start:%d.%m.%Y} (запись №{b['id']}). "
                    f"Выберите другое время или другого мастера.")
    return None

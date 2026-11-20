"""Бизнес-правила записи: рабочее время, запрет записи в прошлое и пересечений."""

from datetime import datetime, time, timedelta

from .models import Booking

WORK_START = time(9, 0)
WORK_END = time(19, 0)


def check_booking(data):
    """Вернуть текст причины отказа или None, если запись допустима."""
    service = data["service"]
    master = data["master"]
    start = datetime.combine(data["date"], data["time"])
    end = start + timedelta(minutes=service.duration_min)

    if start < datetime.now():
        return "Нельзя записаться на прошедшую дату или время."

    if start.time() < WORK_START or end.time() > WORK_END or end.date() != start.date():
        return (f"Автосервис работает с {WORK_START:%H:%M} до {WORK_END:%H:%M}. "
                f"Услуга «{service.name}» длится {service.duration_min} мин "
                f"и не помещается в рабочий день при начале в {start:%H:%M}.")

    if not master.services.filter(pk=service.pk).exists():
        return (f"Мастер {master.name} не выполняет услугу «{service.name}». "
                f"Его специализация: {master.specialization}.")

    same_day = (Booking.objects.select_related("service")
                .filter(master=master, date=start.date())
                .exclude(status="Отменена"))
    for b in same_day:
        if start < b.end and b.start < end:
            return (f"Мастер {master.name} занят с {b.start:%H:%M} до {b.end:%H:%M} "
                    f"{b.start:%d.%m.%Y} (запись №{b.id}). "
                    f"Выберите другое время или другого мастера.")
    return None

"""Справочники услуг и мастеров.

Без них форма записи не сможет предложить услугу и мастера. Записи на обслуживание
и журнал отказов при этом остаются пустыми: их создаёт только форма.
"""

from django.db import migrations

SERVICES = [
    (1, "Плановое ТО", 120, 4500),
    (2, "Компьютерная диагностика", 60, 1500),
    (3, "Шиномонтаж (4 колеса)", 60, 2400),
    (4, "Замена тормозных колодок", 90, 2000),
    (5, "Развал-схождение", 60, 1800),
]

MASTERS = [
    (1, "Петров Сергей", "ТО и диагностика", [1, 2, 4]),
    (2, "Иванов Алексей", "шиномонтаж и ходовая", [3, 4, 5]),
    (3, "Козлов Дмитрий", "диагностика и электрика", [2]),
]


def load(apps, schema_editor):
    Service = apps.get_model("booking", "Service")
    Master = apps.get_model("booking", "Master")
    for pk, name, duration, price in SERVICES:
        Service.objects.update_or_create(
            pk=pk, defaults={"name": name, "duration_min": duration, "price": price})
    for pk, name, spec, service_ids in MASTERS:
        master, _ = Master.objects.update_or_create(
            pk=pk, defaults={"name": name, "specialization": spec})
        master.services.set(service_ids)
    # Счётчики id продолжаются после вставленных вручную номеров.
    if schema_editor.connection.vendor == "postgresql":
        with schema_editor.connection.cursor() as cur:
            for table in ("service", "master"):
                cur.execute(
                    f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                    f"(SELECT MAX(id) FROM {table}))")


def unload(apps, schema_editor):
    apps.get_model("booking", "Master").objects.all().delete()
    apps.get_model("booking", "Service").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("booking", "0001_initial")]
    operations = [migrations.RunPython(load, unload)]

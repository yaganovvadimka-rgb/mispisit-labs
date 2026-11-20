"""Отдельная таблица уведомлений, без сообщений для прежних записей."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("booking", "0002_reference_data")]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name="ID",
                )),
                ("message", models.TextField(verbose_name="Сообщение")),
                ("created_at", models.DateTimeField(
                    auto_now_add=True, verbose_name="Создано",
                )),
                ("status", models.CharField(
                    choices=[("new", "Новое"), ("read", "Прочитано")],
                    default="new", max_length=10, verbose_name="Статус",
                )),
                ("read_at", models.DateTimeField(
                    blank=True, null=True, verbose_name="Прочитано",
                )),
                ("booking", models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="notification", to="booking.booking",
                    verbose_name="Запись на обслуживание",
                )),
            ],
            options={
                "db_table": "notification",
                "ordering": ["-created_at", "-id"],
            },
        ),
    ]

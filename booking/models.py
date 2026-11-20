"""Услуги, мастера, записи на обслуживание, журнал отказов и уведомления."""

from datetime import datetime, timedelta

from django.db import models


class Service(models.Model):
    """Услуга автосервиса (справочник)."""

    name = models.CharField("Название", max_length=100, unique=True)
    duration_min = models.PositiveIntegerField("Длительность, мин")
    price = models.PositiveIntegerField("Базовая стоимость, ₽")

    class Meta:
        db_table = "service"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Master(models.Model):
    """Мастер автосервиса и услуги, которые он выполняет (справочник)."""

    name = models.CharField("ФИО", max_length=100)
    specialization = models.CharField("Специализация", max_length=100)
    services = models.ManyToManyField(Service, related_name="masters",
                                      db_table="master_service")

    class Meta:
        db_table = "master"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Booking(models.Model):
    """Запись клиента на обслуживание."""

    STATUS_NEW = "Новая"
    STATUS_CHOICES = [
        ("Новая", "Новая"),
        ("Подтверждена", "Подтверждена"),
        ("В работе", "В работе"),
        ("Выполнена", "Выполнена"),
        ("Отменена", "Отменена"),
    ]

    client_name = models.CharField("Имя клиента", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    car = models.CharField("Автомобиль", max_length=100)
    plate = models.CharField("Госномер", max_length=12)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="bookings")
    master = models.ForeignKey(Master, on_delete=models.PROTECT, related_name="bookings")
    date = models.DateField("Дата")
    time = models.TimeField("Время начала")
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES,
                              default=STATUS_NEW)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        db_table = "booking"
        ordering = ["date", "time"]
        indexes = [models.Index(fields=["master", "date"])]

    @property
    def start(self):
        return datetime.combine(self.date, self.time)

    @property
    def end(self):
        return self.start + timedelta(minutes=self.service.duration_min)


class Rejection(models.Model):
    """Попытка записи, которую система не приняла, и причина отказа."""

    client_name = models.CharField("Кто пытался", max_length=100)
    action = models.CharField("Действие", max_length=100, default="Запись на обслуживание")
    service_name = models.CharField("Услуга", max_length=100)
    master_name = models.CharField("Мастер", max_length=100)
    requested = models.CharField("Желаемые дата и время", max_length=40)
    reason = models.TextField("Причина отказа")
    created_at = models.DateTimeField("Когда", auto_now_add=True)

    class Meta:
        db_table = "rejection"
        ordering = ["-id"]


class Notification(models.Model):
    """Сохранённое уведомление сотруднику об успешной записи клиента."""

    STATUS_NEW = "new"
    STATUS_READ = "read"
    STATUS_CHOICES = [(STATUS_NEW, "Новое"), (STATUS_READ, "Прочитано")]

    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name="notification",
        verbose_name="Запись на обслуживание",
    )
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    status = models.CharField(
        "Статус", max_length=10, choices=STATUS_CHOICES, default=STATUS_NEW,
    )
    read_at = models.DateTimeField("Прочитано", null=True, blank=True)

    class Meta:
        db_table = "notification"
        ordering = ["-created_at", "-id"]

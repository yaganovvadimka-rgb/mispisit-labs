"""Форма записи клиента на обслуживание."""

import re

from django import forms

from .models import Master, Service

PLATE_RE = re.compile(r"^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}$")


class BookingForm(forms.Form):
    client_name = forms.CharField(label="Имя клиента", max_length=100)
    phone = forms.CharField(label="Телефон", max_length=20,
                            widget=forms.TextInput(attrs={"type": "tel"}))
    car = forms.CharField(label="Автомобиль (марка и модель)", max_length=100)
    plate = forms.CharField(label="Госномер", max_length=12,
                            help_text="Например: А123ВС73")
    service = forms.ModelChoiceField(label="Услуга", queryset=Service.objects.all(),
                                     empty_label="— выберите услугу —")
    master = forms.ModelChoiceField(label="Мастер", queryset=Master.objects.all(),
                                    empty_label="— выберите мастера —")
    date = forms.DateField(label="Дата", widget=forms.DateInput(attrs={"type": "date"}))
    time = forms.TimeField(label="Время", widget=forms.TimeInput(attrs={"type": "time", "step": 1800}))
    comment = forms.CharField(label="Комментарий", required=False,
                              widget=forms.Textarea(attrs={"rows": 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].label_from_instance = (
            lambda s: f"{s.name} ({s.duration_min} мин, от {s.price} ₽)")
        self.fields["master"].label_from_instance = (
            lambda m: f"{m.name} — {m.specialization}")
        for name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            )
            if field.help_text:
                field.widget.attrs["aria-describedby"] = f"id_{name}_helptext"
        self.fields["client_name"].widget.attrs.update(
            {"placeholder": "Иван Петров", "autocomplete": "name"})
        self.fields["phone"].widget.attrs.update(
            {"placeholder": "+7 917 123-45-67", "autocomplete": "tel"})
        self.fields["car"].widget.attrs["placeholder"] = "Lada Vesta"
        self.fields["plate"].widget.attrs["placeholder"] = "А123ВС73"
        self.fields["comment"].widget.attrs["placeholder"] = "Что мастеру нужно знать перед визитом?"

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = re.sub(r"\D", "", phone)
        if len(digits) != 11 or digits[0] not in "78":
            raise forms.ValidationError(
                "телефон должен содержать 11 цифр, например +7 917 123-45-67")
        return phone

    def clean_plate(self):
        plate = self.cleaned_data["plate"].upper().replace(" ", "")
        # Латинские буквы, похожие на кириллические, приводим к кириллице.
        plate = plate.translate(str.maketrans("ABEKMHOPCTYX", "АВЕКМНОРСТУХ"))
        if not PLATE_RE.match(plate):
            raise forms.ValidationError("госномер должен быть в формате А123ВС73")
        return plate

"""Чтение и запись демо-данных в JSON-файлах папки data/."""

import json
import os
import tempfile
import threading

from django.conf import settings

_lock = threading.Lock()


def _path(name):
    return settings.DATA_DIR / f"{name}.json"


def load(name):
    """Прочитать список объектов из data/<name>.json."""
    with _lock:
        with open(_path(name), encoding="utf-8") as f:
            return json.load(f)


def _save(name, items):
    path = _path(name)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def append(name, item):
    """Добавить объект в файл и присвоить ему следующий номер id."""
    with _lock:
        with open(_path(name), encoding="utf-8") as f:
            items = json.load(f)
        item["id"] = max((i["id"] for i in items), default=0) + 1
        items.append(item)
        _save(name, items)
        return item


def services():
    return {s["id"]: s for s in load("services")}


def masters():
    return {m["id"]: m for m in load("masters")}

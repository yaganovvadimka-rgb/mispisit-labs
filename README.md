# Система онлайн-записи в автосервис

Веб-кабинет сотрудника автосервиса для записи клиентов на обслуживание,
просмотра записей, причин отказов и уведомлений. Версия приложения: **0.0.5**.
Лабораторные работы по дисциплине МиСПИСИТ.

Стек: Python 3.13, Django 5.2.19, Django Templates, Bootstrap 5.3.9,
HTML/CSS, PostgreSQL 16, Django ORM.

## Запуск

```text
Репозиторий: https://github.com/yaganovvadimka-rgb/mispisit-labs
Ветка: lab5
Pull Request: [https://github.com/yaganovvadimka-rgb/mispisit-labs/pull/5](https://github.com/yaganovvadimka-rgb/mispisit-labs/pull/5)
Образ: yaganovvadimkargb/mispisit-labs:0.0.5
```

Страница образа: [https://hub.docker.com/r/yaganovvadimkargb/mispisit-labs](https://hub.docker.com/r/yaganovvadimkargb/mispisit-labs)

Для запуска нужен Docker с поддержкой Docker Compose.

```sh
git clone -b lab5 https://github.com/yaganovvadimka-rgb/mispisit-labs
cd mispisit-labs
docker compose up -d
```

После запуска сайт открывается по адресу [http://localhost:8080](http://localhost:8080).
Структура базы создаётся автоматически миграциями Django. При первом запуске с новым
томом список записей, журнал отказов и уведомления пустые, демонстрационные записи не загружаются.
Справочники услуг и мастеров заполняются автоматически миграцией.

## Страницы

| Адрес | Что на странице |
| --- | --- |
| [http://localhost:8080/](http://localhost:8080/) | Главная кабинета сотрудника, версия приложения, количество записей и отказов, услуги и переходы к действиям |
| [http://localhost:8080/bookings/](http://localhost:8080/bookings/) | Список записей на обслуживание: клиент, автомобиль, услуга, мастер, дата, время и статус; до первой записи — пустое состояние с кнопкой создания записи |
| [http://localhost:8080/bookings/new/](http://localhost:8080/bookings/new/) | Форма записи: данные клиента и автомобиля, услуга, мастер, дата, время и комментарий |
| `http://localhost:8080/bookings/<id>/` | Карточка записи: данные клиента и автомобиля, услуга, мастер, время визита и статус; вместо `<id>` указывается номер записи |
| [http://localhost:8080/bookings/rejected/](http://localhost:8080/bookings/rejected/) | Причина отказа и журнал отклонённых попыток: кто, что пытался сделать и почему запись не создана; до первого отказа — пустой журнал |
| [http://localhost:8080/notifications/](http://localhost:8080/notifications/) | Уведомления сотруднику о новых записях: номер записи, клиент, автомобиль, услуга, мастер, время визита и статус прочтения |

Данные хранятся в PostgreSQL (сервис `db`, том `dbdata`). После `docker compose down`
и `docker compose up -d` записи сохраняются. Флаг `-v` у команды `docker compose down`
удаляет том вместе со всеми данными базы.

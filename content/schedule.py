import csv
from datetime import date, datetime, timedelta
import calendar
import locale
locale.getlocale()
locale.setlocale(locale.LC_ALL, 'de_DE')

events = list()

with open("content/events.csv") as events_file:
    reader = csv.DictReader(events_file)
    for row in reader:
        events.append(
            {
                "date": datetime.fromisoformat(row["date"]),
                "event_type": row["event_type"],
                "name": row["name"],
                "link": row["link"]
            }
        )


def is_in_sommerpause(termin: datetime) -> bool:
    return termin >= datetime(2025, 5, 15) and termin <= datetime(2025, 8, 15)


def is_himmelsbeobachtung(termin: datetime) -> bool:
    # get a calendar for the month of the given date
    month_calendar = calendar.monthcalendar(termin.year, termin.month)

    # assemble a list of fridays this month
    fridays = list()
    for week in month_calendar:
        day_of_friday = week[calendar.FRIDAY]
        if day_of_friday != 0:
            fridays.append(day_of_friday)

    himmelsbeobachtung_termine = list()
    first_friday = datetime(termin.year, termin.month, fridays[0])

    if not is_in_sommerpause(first_friday):
        himmelsbeobachtung_termine.append(first_friday)

    third_friday = datetime(termin.year, termin.month,
                            fridays[2]) if len(fridays) >= 3 else None

    if third_friday is not None and not is_in_sommerpause(first_friday):
        himmelsbeobachtung_termine.append(third_friday)

    for himmelsbeobachtung_termin in himmelsbeobachtung_termine:
        if himmelsbeobachtung_termin == termin:
            return True

    return False


def is_sonnenbeobachtung(termin: datetime) -> bool:
    if termin.month >= 3 and termin.month <= 9:
        # summer
        pass
    else:
        # winter
        pass
    return False


def is_on_google_schedule(termin: datetime) -> tuple[bool, str | None]:
    if termin.weekday() == 4:
        return True, "himmelsbeobachtung"
    if termin.weekday() == 6:
        return True, "sonnenbeobachtung"
    return False, None


def is_a_scheduled_event(termin: datetime) -> tuple[bool, str | None]:
    for event in events:
        if termin.date() == event["date"].date():
            return True, event["event_type"]
    return False, None


current_date = datetime(2025, 5, 1)
end_date = datetime(2025, current_date.month + 4, 1) - timedelta(days=1)
print(f"From {current_date.strftime("%A, %x")} to {end_date.strftime("%A, %x")}")

while current_date <= end_date:
    if current_date.day == 1:
        print(f"--- {current_date.strftime("%B")} ---")
    notify = False
    is_scheduled, scheduled_event_type = is_a_scheduled_event(current_date)
    is_scheduled_google, scheduled_event_type_google = is_on_google_schedule(
        current_date)

    should_be_closed = not is_scheduled and is_scheduled_google
    should_be_opened = is_scheduled and not is_scheduled_google
    should_be_extended = scheduled_event_type == "vhs" and scheduled_event_type_google == "himmelsbeobachtung"

    if should_be_closed or should_be_opened or should_be_extended:
        print(f"{current_date.strftime("%A, %x")}:")

    if scheduled_event_type != scheduled_event_type_google:
        print(
            f" Mismatch! Scheduled event: {scheduled_event_type}, Google: {scheduled_event_type_google}")

    if should_be_closed:
        print(" Should be closed")

    if should_be_opened:
        print(f" Should be opened. Event Type: {scheduled_event_type}")

    if should_be_extended:
        print(
            f" Should be extended. Google: {scheduled_event_type_google}, but should be {scheduled_event_type}")

    current_date += timedelta(days=1)

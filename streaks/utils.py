import calendar
from journal.models import Journal
from streaks.models import StreakSaverUse, UserBadge, Badge
from datetime import datetime, timedelta, date
from django.utils import timezone


def get_month_days(year, month):
    days = calendar.monthrange(year, month)[1]
    return [date(year, month, day) for day in range(1, days + 1)]


def get_week_days():
    today = datetime.today().date()
    start_date = today - timedelta(days=6)
    return [start_date + timedelta(days=x) for x in range(0, 7)]


def get_calendar_data(streak, year, month):
    start_date = streak.start_date
    current_date = datetime.today().date()
    use_saver_by, can_use_saver_after = None, None

    # Update streak if not updated recently
    if streak.last_entry_date < current_date - timedelta(days=2):
        streak.current_streak = 0
        streak.start_date = current_date
        streak.save()

    # Get a list of days for which we need to return data
    if year and month:
        days = get_month_days(year, month)
    else:
        days = get_week_days()
    calendar_start_date = days[0]

    # If streak start date is less than the calendar start date, we need to add extra
    # days to the start of the calendar for calculations of
    # use_saver_by, can_use_saver_after and is_frozen
    if start_date < calendar_start_date:
        for i in range(7):
            days.insert(0, calendar_start_date - timedelta(days=i + 1))

    # lists of dates on which entries were made, streak saver was used, and badges were earnZ
    entries = (
        Journal.objects.filter(
            user_id=streak.user_id,
            created_at__range=[days[0], days[-1] + timedelta(days=1)],
        )
        .order_by("created_at")
        .values_list("created_at__date", flat=True)
    )
    streak_saver_used_dates = (
        StreakSaverUse.objects.filter(
            user_id=streak.user_id, created_at__range=[days[0], days[-1]]
        )
        .order_by("created_at")
        .values_list("created_at__date", flat=True)
    )
    badges_earned = (
        UserBadge.objects.filter(
            user_id=streak.user_id,
            created_at__range=[days[0], days[-1] + timedelta(days=1)],
        )
        .order_by("created_at")
        .values_list("created_at__date", "badge_id")
    )

    days_missed_in_current_streak_week = 0
    days_data = []
    is_frozen = False
    for day in days:
        entry_count = entries.filter(created_at__date=day).count()
        streak_saver_used = streak_saver_used_dates.filter(
            created_at__date=day
        ).exists()

        # Add day data to the list
        if day >= calendar_start_date:
            day_data = {
                "date": day,
                "day": day.day,
                "entry_count": entry_count,
                "streak_saver_used": streak_saver_used,
                "badge_earned": badges_earned.filter(created_at__date=day).exists()
                and Badge.objects.get(id=badges_earned.get(created_at__date=day)[1])
                or None,
                "in_current_streak": start_date <= day <= current_date,
                "is_frozen": is_frozen and entry_count,
            }
            days_data.append(day_data)

        # Calculations for missed day in current streak and frozen
        if current_date > day >= max(start_date, current_date - timedelta(days=6)):
            if entry_count == 0 and not streak_saver_used:
                days_missed_in_current_streak_week += 1
                missed_date = day
                is_frozen = True

        # Calculations for the date after which streak saver can be used again
        if streak_saver_used and day + timedelta(days=6) > current_date:
            can_use_saver_after = day + timedelta(days=6)

    if days_missed_in_current_streak_week:
        use_saver_by = missed_date + timedelta(days=6)

    calendar_data = {
        "current_date": current_date,
        "use_saver_by": use_saver_by,
        "can_use_saver_after": can_use_saver_after,
        "days_data": days_data,
    }

    return calendar_data


def update_streak_function(streak):
    today = datetime.now().date()
    update_current_streak_and_start_date(streak)
    streak.highest_streak = max(streak.current_streak, streak.highest_streak)
    streak.last_entry_date = today
    streak.save()
    return streak


def update_current_streak_and_start_date(streak):
    today = datetime.now().date()
    start_date = streak.start_date
    one_week_ago = today - timedelta(days=6)
    prev_week_last_day = one_week_ago - timedelta(days=1)
    prev_week_second_last_day = one_week_ago - timedelta(days=2)

    if streak.last_entry_date < today - timedelta(days=2):
        streak.current_streak = 1
        streak.start_date = today
        return streak

    else:
        days = []
        for i in range(8):
            days.append(today - timedelta(days=i))

        entries = (
            Journal.objects.filter(
                user_id=streak.user_id,
                created_at__range=[
                    prev_week_second_last_day,
                    today + timedelta(days=1),
                ],
            )
            .order_by("created_at")
            .values_list("created_at__date", flat=True)
        )
        streak_saver_used_dates = (
            StreakSaverUse.objects.filter(
                user_id=streak.user_id,
                created_at__range=[
                    prev_week_second_last_day,
                    today + timedelta(days=1),
                ],
            )
            .order_by("created_at")
            .values_list("created_at__date", flat=True)
        )

        if (
            prev_week_last_day >= start_date
            and prev_week_last_day not in entries
            and prev_week_last_day not in streak_saver_used_dates
        ):
            start_date = prev_week_last_day + timedelta(days=1)
        elif (
            prev_week_second_last_day >= start_date
            and prev_week_second_last_day not in entries
            and prev_week_second_last_day not in streak_saver_used_dates
        ):
            start_date = prev_week_second_last_day + timedelta(days=1)

        entries_missed_in_streak = 0
        entry_miss_date = None
        for day in days:
            if day not in entries and day not in streak_saver_used_dates:
                if day >= start_date:
                    entries_missed_in_streak += 1
                    if entries_missed_in_streak == 2:
                        start_date = day + timedelta(days=1)
                        break
                    else:
                        entry_miss_date = day

        streak.current_streak = (
            (entry_miss_date - start_date).days
            if entry_miss_date
            else (today - start_date).days + 1
        )
        streak.start_date = start_date

        return streak


def get_streak_saving_date(streak):
    today = timezone.now().date()
    streak_start_date = streak.start_date
    one_week_ago = today - timedelta(days=6)
    start_date = max(streak_start_date, one_week_ago)
    if start_date == today:
        return None
    entry_dates = (
        Journal.objects.filter(
            user_id=streak.user_id,
            created_at__range=[start_date, today],
        )
        .order_by("created_at")
        .values_list("created_at__date", flat=True)
    )
    missed_days, missed_date = 0, None
    while start_date < today:
        if start_date not in entry_dates:
            missed_days += 1
            missed_date = start_date
        start_date += timedelta(days=1)
    if missed_days == 1:
        return datetime.combine(missed_date, datetime.min.time())
    return None

from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from datetime import datetime, timedelta

async def safe_edit_text(message, *args, **kwargs):
    try:
        await message.edit_text(*args, **kwargs)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass  # игнорируем
        else:
            raise

async def safe_edit_reply_markup(message, *args, **kwargs):
    try:
        await message.edit_reply_markup(*args, **kwargs)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise

def pretty_calendar_markup(
    state="date",
    year=None,
    month=None,
    available_days=None,
    admin_mode=False,
    selected_day=None
):
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    today = now.date()
    first_day = datetime(year, month, 1)
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    days_in_month = (next_month - timedelta(days=1)).day
    week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

    kb = InlineKeyboardBuilder()
    # Верхняя строка: год, месяц, навигация
    kb.row(
        InlineKeyboardButton(text=f"{year}", callback_data="ignore"),
        InlineKeyboardButton(text=f"{first_day.strftime('%B')}", callback_data="ignore"),
        InlineKeyboardButton(text="◀️", callback_data=f"{state}_m_{year}_{month-1 if month > 1 else 12}"),
        InlineKeyboardButton(text="▶️", callback_data=f"{state}_m_{year}_{month+1 if month < 12 else 1}"),
    )
    # День недели
    kb.row(*[InlineKeyboardButton(text=d, callback_data="ignore") for d in week_days])
    row = []
    # Сдвиг для первого дня недели
    week_shift = (first_day.weekday() + 6) % 7
    for _ in range(week_shift):
        row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
    for day in range(1, days_in_month + 1):
        d = datetime(year, month, day)
        is_past = d.date() < today
        date_str = f"{year}-{month:02d}-{day:02d}"
        wday = d.weekday()
        # 5 - суббота, 6 - воскресенье
        if is_past and (year, month) == (today.year, today.month):
            # Прошедшие дни — пустые
            row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
        else:
            text = f"{day}"
            # Сегодня
            if d.date() == today:
                text = f"🟡{day}"
            # Рабочий день
            elif available_days and date_str in available_days:
                text = f"🟢{day}"
            # Выходные (если не рабочий день)
            elif wday in (5, 6) and (not available_days or date_str not in available_days):
                text = f"❌"
            # Остальное — стандартно
            if selected_day == day:
                text = f"[{text}]"
            cb_data = f"{state}_d_{year}_{month}_{day}" if ((not is_past or admin_mode) and text != "❌") else "ignore"
            row.append(InlineKeyboardButton(text=text, callback_data=cb_data))
        if len(row) == 7:
            kb.row(*row)
            row = []
    if row:
        while len(row) < 7:
            row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
        kb.row(*row)
    kb.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"{state}_back"))
    if admin_mode:
        kb.row(InlineKeyboardButton(text="✅ Готово", callback_data="admin_done"))
    return kb.as_markup()
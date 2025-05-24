import os
import time
import sqlite3
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "secret123")
ADMIN_SESSION_TIMEOUT = 3600  # 1 hour

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

ADMIN_SESSIONS = {}  # user_id: timestamp

DB_FILE = "booking_bot.db"
TIME_SLOTS = [
    "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
    "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
    "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
    "17:00", "17:30"
]

def get_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    return conn, cur

def init_db():
    conn, cur = get_db()
    # Таблица для записей
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        username TEXT,
        date TEXT,
        time TEXT,
        confirmed INTEGER DEFAULT 0
    )""")
    # Таблица для выходных
    cur.execute("""
    CREATE TABLE IF NOT EXISTS weekends (
        id INTEGER PRIMARY KEY,
        day TEXT
    )""")
    conn.commit()
    conn.close()

def is_admin_session(user_id):
    now = time.time()
    ts = ADMIN_SESSIONS.get(user_id)
    if ts and now - ts < ADMIN_SESSION_TIMEOUT:
        return True
    if ts:
        ADMIN_SESSIONS.pop(user_id)
    return False

def main_menu(is_admin=False):
    kb = InlineKeyboardBuilder()
    kb.button(text="🗓️ Записаться", callback_data="book")
    kb.button(text="🩺 Проверка бота", callback_data="selfcheck")
    if is_admin:
        kb.button(text="📅 Рабочие дни", callback_data="workdays")
        kb.button(text="🚫 Выходные", callback_data="weekends")
        kb.button(text="📋 Подтвердить записи", callback_data="admin_bookings")
        kb.button(text="🚪 Выйти из режима администратора", callback_data="exitadmin")
    kb.adjust(1)
    return kb.as_markup()

def time_markup(times):
    kb = InlineKeyboardBuilder()
    for t in times:
        kb.button(text=f"⏰ {t}", callback_data=f"time_{t}")
    kb.adjust(1)  # по одной кнопке в строке!
    kb.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="time_back"))
    return kb.as_markup()

@router.message(Command("start"))
async def start(msg: Message):
    await msg.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=main_menu(is_admin=is_admin_session(msg.from_user.id))
    )

@router.message(Command("admin"))
async def admin_entry(msg: Message):
    await msg.answer("Введите пароль администратора:")

@router.message(lambda m: m.text and m.text.lower().startswith("пароль:"))
async def admin_password(msg: Message):
    pwd = msg.text.split(":", 1)[1].strip()
    if pwd == ADMIN_PASSWORD:
        ADMIN_SESSIONS[msg.from_user.id] = time.time()
        await msg.answer("✅ Вы вошли в режим администратора!", reply_markup=main_menu(is_admin=True))
    else:
        await msg.answer("❌ Неверный пароль.")

@router.callback_query(F.data == "exitadmin")
@router.message(Command("exitadmin"))
async def admin_logout(msg: Message | CallbackQuery):
    user_id = msg.from_user.id if isinstance(msg, Message) else msg.from_user.id
    ADMIN_SESSIONS.pop(user_id, None)
    if isinstance(msg, CallbackQuery):
        await msg.message.edit_text("Вы вышли из режима администратора.", reply_markup=main_menu())
    else:
        await msg.answer("Вы вышли из режима администратора.", reply_markup=main_menu())

@router.callback_query(F.data == "selfcheck")
async def self_check(cb: CallbackQuery):
    # ОДИН цикл проверки!
    status = []
    # Проверка .env
    if not API_TOKEN:
        status.append("❌ Нет TELEGRAM_BOT_TOKEN")
    else:
        status.append("✅ TELEGRAM_BOT_TOKEN найден")
    # Проверка базы
    try:
        conn, cur = get_db()
        cur.execute("SELECT 1 FROM bookings LIMIT 1")
        status.append("✅ БД ok")
    except Exception as e:
        status.append(f"❌ БД: {e}")
    finally:
        try:
            conn.close()
        except: pass
    await cb.answer("Проверка завершена", show_alert=True)
    await cb.message.answer("🩺 Self-check:\n" + "\n".join(status))

@router.callback_query(F.data == "book")
async def book_start(cb: CallbackQuery):
    # Сюда можно сделать выбор даты, пока демо — сразу выбор времени на 2025-05-29
    await cb.message.edit_text("Вы выбрали 2025-05-29.\nТеперь выберите время:", reply_markup=time_markup(TIME_SLOTS))

@router.callback_query(lambda c: c.data and c.data.startswith("time_"))
async def time_selected(cb: CallbackQuery):
    time_slot = cb.data.replace("time_", "")
    # Запись в БД с confirmed=0
    conn, cur = get_db()
    cur.execute("INSERT INTO bookings (user_id, username, date, time, confirmed) VALUES (?, ?, ?, ?, 0)",
                (cb.from_user.id, cb.from_user.username, "2025-05-29", time_slot))
    conn.commit()
    conn.close()
    await cb.message.edit_text(f"⏰ Вы записаны на {time_slot}. Ожидайте подтверждения парикмахером!")

@router.callback_query(F.data == "admin_bookings")
async def admin_bookings(cb: CallbackQuery):
    if not is_admin_session(cb.from_user.id):
        await cb.answer("Нет прав", show_alert=True)
        return
    conn, cur = get_db()
    cur.execute("SELECT id, user_id, username, date, time FROM bookings WHERE confirmed=0")
    rows = cur.fetchall()
    if not rows:
        await cb.message.edit_text("Нет неподтверждённых записей.", reply_markup=main_menu(is_admin=True))
        return
    kb = InlineKeyboardBuilder()
    text = "Неподтверждённые записи:\n"
    for row in rows:
        bid, uid, uname, date, time_slot = row
        kb.button(text=f"Подтвердить {time_slot} для @{uname or uid}", callback_data=f"confirm_{bid}")
        text += f"{date} {time_slot} @{uname or uid}\n"
    kb.adjust(1)
    kb.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_admin"))
    await cb.message.edit_text(text, reply_markup=kb.as_markup())

@router.callback_query(lambda c: c.data and c.data.startswith("confirm_"))
async def confirm_booking(cb: CallbackQuery):
    if not is_admin_session(cb.from_user.id):
        await cb.answer("Нет прав", show_alert=True)
        return
    bid = int(cb.data.replace("confirm_", ""))
    conn, cur = get_db()
    cur.execute("UPDATE bookings SET confirmed=1 WHERE id=?", (bid,))
    cur.execute("SELECT user_id, date, time FROM bookings WHERE id=?", (bid,))
    user_id, date, time_slot = cur.fetchone()
    conn.commit()
    conn.close()
    await bot.send_message(user_id, f"Ваша запись на {date} {time_slot} подтверждена парикмахером!")
    await cb.answer("Запись подтверждена")
    await admin_bookings(cb)

@router.callback_query(F.data == "back_admin")
async def back_admin(cb: CallbackQuery):
    await cb.message.edit_text("Меню администратора:", reply_markup=main_menu(is_admin=True))

@router.callback_query(F.data == "weekends")
async def weekends_admin(cb: CallbackQuery):
    if not is_admin_session(cb.from_user.id):
        await cb.answer("Нет прав", show_alert=True)
        return
    # Показываем календарь, для простоты — текущий месяц
    import calendar, datetime
    now = datetime.datetime.now()
    year, month = now.year, now.month
    c = calendar.monthcalendar(year, month)
    kb = InlineKeyboardBuilder()
    text = f"Выделите выходные {calendar.month_name[month]} {year}:\n"
    for week in c:
        for day in week:
            if day == 0:
                kb.button(text=" ", callback_data="noop")
            else:
                kb.button(text=str(day), callback_data=f"toggle_weekend_{year}_{month}_{day}")
    kb.adjust(7)
    kb.row(InlineKeyboardButton(text="Сохранить", callback_data="save_weekends"))
    kb.row(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_admin"))
    await cb.message.edit_text(text, reply_markup=kb.as_markup())

@router.callback_query(lambda c: c.data and c.data.startswith("toggle_weekend_"))
async def toggle_weekend(cb: CallbackQuery):
    # Сохранять/удалять выходной в БД
    _, y, m, d = cb.data.split("_")[2:]
    date = f"{y}-{int(m):02d}-{int(d):02d}"
    conn, cur = get_db()
    cur.execute("SELECT 1 FROM weekends WHERE day=?", (date,))
    if cur.fetchone():
        cur.execute("DELETE FROM weekends WHERE day=?", (date,))
        await cb.answer(f"{date} убран из выходных")
    else:
        cur.execute("INSERT INTO weekends(day) VALUES (?)", (date,))
        await cb.answer(f"{date} добавлен в выходные")
    conn.commit()
    conn.close()
    await weekends_admin(cb)

@router.callback_query(F.data == "save_weekends")
async def save_weekends(cb: CallbackQuery):
    await cb.answer("Выходные сохранены", show_alert=True)
    await cb.message.edit_text("Меню администратора:", reply_markup=main_menu(is_admin=True))

# Инициализация базы при старте
init_db()

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
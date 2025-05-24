from aiogram.fsm.storage.memory import MemoryStorage

ADMIN_PASSWORD = "your_secret_password"
ADMIN_SESSIONS = set()

@router.message(commands=["admin"])
async def admin_login(msg: Message):
    await msg.answer("Введите пароль администратора:")

@router.message(lambda m: m.text and m.text.startswith("Пароль:"))
async def admin_password_check(msg: Message):
    pwd = msg.text.replace("Пароль:", "").strip()
    if pwd == ADMIN_PASSWORD:
        ADMIN_SESSIONS.add(msg.from_user.id)
        await msg.answer("✅ Вы вошли в режим администратора!", reply_markup=admin_menu())
    else:
        await msg.answer("❌ Неверный пароль.")

@router.message(commands=["exitadmin"])
async def admin_logout(msg: Message):
    ADMIN_SESSIONS.discard(msg.from_user.id)
    await msg.answer("Вы вышли из режима администратора.", reply_markup=main_menu())

def is_admin_session(user_id):
    return user_id in ADMIN_SESSIONS

def admin_menu():
    # Вернуть клавиатуру с админскими функциями
    pass

def main_menu():
    # Обычное меню
    pass
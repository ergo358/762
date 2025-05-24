ADMIN_PASSWORD = "your_secret_password"
ADMIN_SESSIONS = {}  # user_id: timestamp

ADMIN_SESSION_TIMEOUT = 3600  # 1 час

def is_admin_session(user_id):
    # Проверка, не истекла ли сессия
    import time
    now = time.time()
    ts = ADMIN_SESSIONS.get(user_id)
    if ts and now - ts < ADMIN_SESSION_TIMEOUT:
        return True
    if ts:
        ADMIN_SESSIONS.pop(user_id)
    return False

@router.message(commands=["admin"])
async def admin_login(msg: Message):
    await msg.answer("Введите пароль администратора:")

@router.message(lambda m: m.text and m.text.lower().startswith("пароль:"))
async def admin_password_check(msg: Message):
    pwd = msg.text.split(":", 1)[1].strip()
    if pwd == ADMIN_PASSWORD:
        import time
        ADMIN_SESSIONS[msg.from_user.id] = time.time()
        await msg.answer("✅ Вы вошли в режим администратора!", reply_markup=admin_menu())
    else:
        await msg.answer("❌ Неверный пароль.")

@router.message(commands=["exitadmin"])
async def admin_logout(msg: Message):
    ADMIN_SESSIONS.pop(msg.from_user.id, None)
    await msg.answer("Вы вышли из режима администратора.", reply_markup=main_menu())

# Все админские функции теперь используют is_admin_session(user_id)
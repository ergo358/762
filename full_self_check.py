def validate_telegram_token(token):
    import re
    return re.match(r"^[0-9]+:.*$", token or "")

def full_self_check():
    checks = []
    # 1. .env
    if not os.path.exists(".env"):
        checks.append("❌ .env не найден!")
    else:
        checks.append("✅ .env найден.")
    # 2. Переменные
    from dotenv import dotenv_values
    env = dotenv_values(".env")
    REQUIRED = ["TELEGRAM_BOT_TOKEN"]
    for var in REQUIRED:
        if var not in env or not env[var]:
            checks.append(f"❌ Переменная {var} не указана или пуста!")
        else:
            checks.append(f"✅ {var} задана.")
    # 3. Токен
    token = env.get("TELEGRAM_BOT_TOKEN", "")
    if not validate_telegram_token(token):
        checks.append("⚠️ TELEGRAM_BOT_TOKEN выглядит подозрительно. Проверьте формат.")
    # 4. БД
    if not os.path.exists("booking_bot.db"):
        checks.append("❌ booking_bot.db не найден!")
    else:
        try:
            import sqlite3
            conn = sqlite3.connect("booking_bot.db")
            cur = conn.cursor()
            for table in ["bookings", "workdays"]:
                cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if not cur.fetchone():
                    checks.append(f"❌ Таблица {table} отсутствует в БД!")
                else:
                    checks.append(f"✅ Таблица {table} есть.")
            conn.close()
        except Exception as e:
            checks.append(f"❌ Ошибка при работе с БД: {e}")
    # 5. facade.jpg
    if not os.path.exists("facade.jpg"):
        checks.append("⚠️ facade.jpg не найден (будет заглушка).")
    else:
        if os.path.getsize("facade.jpg") > 5*1024*1024:
            checks.append("⚠️ facade.jpg больше 5 МБ!")
        else:
            checks.append("✅ facade.jpg найден и нормального размера.")
    # 6. Версии
    try:
        import aiogram
        import python_dotenv
        checks.append(f"✅ aiogram {aiogram.__version__}, python-dotenv {python_dotenv.__version__}")
    except Exception as e:
        checks.append(f"❌ Проблема с зависимостями: {e}")
    # 7. ADMIN_IDS
    try:
        from telegram_booking_bot import ADMIN_IDS
        if not ADMIN_IDS or not all(isinstance(x, int) for x in ADMIN_IDS):
            checks.append("⚠️ ADMIN_IDS не заполнено или содержит не числа!")
        else:
            checks.append("✅ ADMIN_IDS корректно.")
    except Exception:
        checks.append("⚠️ Не удалось проверить ADMIN_IDS.")
    # 8. README.md
    if not os.path.exists("README.md"):
        checks.append("⚠️ README.md отсутствует.")
    else:
        checks.append("✅ README.md найден.")
    # 9. Календарь (логика)
    # Тут можно добавить спец.проверку, если понадобится
    return "\n".join(checks)
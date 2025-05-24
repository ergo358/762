import os
import asyncio
import random
import aiohttp

# Примерный сценарий нагрузочного теста — имитирует работу 100 пользователей
# Этот файл не для запуска вместе с ботом, а для отдельного тестирования API или webhook (если реализовано).
# Для настоящего Telegram API нужно использовать тестовые аккаунты и Telegram Bot API.
# Этот скрипт — шаблон, его надо доработать под ваш endpoint или тестовые ручки.

async def fake_user(session, user_id):
    # Симуляция действий пользователя: запись, лайк, отзыв
    # Здесь вы должны реализовать вызовы через API или вебхуки к вашему боту (если есть)
    # Пример для REST API, если бы он был:
    # await session.post("http://localhost:8080/api/book", json={...})
    await asyncio.sleep(random.uniform(0.1, 0.5))  # симуляция времени между действиями

async def main():
    users = 100
    async with aiohttp.ClientSession() as session:
        tasks = [fake_user(session, i) for i in range(users)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
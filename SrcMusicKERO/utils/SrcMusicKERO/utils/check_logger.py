from pyrogram import Client
import config
import asyncio

app = Client("test_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

async def check_logger():
    async with app:
        try:
            chat = await app.get_chat(config.LOGGER_ID)
            print(f"✔ المجموعة موجودة: {chat.title} (ID: {chat.id})")
        except Exception as e:
            print(f"❌ خطأ في الوصول للمجموعة: {e}")

if __name__ == "__main__":
    asyncio.run(check_logger())

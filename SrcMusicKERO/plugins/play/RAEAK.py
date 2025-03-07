import asyncio
from pyrogram import Client, filters
from random import choice
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from SrcMusicKERO import app

RAEAK = ["فاجره","حلوه","فخامه","جميله","خوش","جميله","يععععع","وحشه","مش حلوه","حلوه ياعم","خليك بيها","حبتها","غيرها يعم"]

@app.on_message(filters.command(["صورتي", "✨ رايك بصورتي", "صورتي"]))
async def madison(client: Client, message: Message):
    usr = await client.get_users(message.from_user.id)
    name = usr.first_name
    try:
        async for photo in client.iter_profile_photos(message.from_user.id, limit=1):
            await message.reply_photo(photo.file_id, caption=f"صورتك {choice(RAEAK)} 🐉", 
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(name, url=f"https://t.me/{message.from_user.username}")]
                ]
            ))
    except Exception as e:
        await message.reply_text("لا أستطيع العثور على صورة لك.")

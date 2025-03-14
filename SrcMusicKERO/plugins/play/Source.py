import asyncio
import os
import time
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# استيراد السورس والمكتبات الأخرى
from SrcMusicKERO import app

# ⬇️ إرسال صورة السورس
@app.on_message(filters.command(["✨ سورس", "مطور السورس", "السورس"]))
async def send_source_image(client: Client, message: Message):
    await message.reply_photo(
        photo="https://envs.sh/ws4.webp",  # ضع رابط الصورة هنا
        caption="⍟ 𝚃𝙷𝙴 𝙱𝙴𝚂𝚃 𝚂𝙾𝚄𝚁𝙲𝙴 𝙾𝙽 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("مـطور السـورس", url="https://t.me/Fox4566"),
                    InlineKeyboardButton("مبرمج السورس", url="https://t.me/Loo_la3")
                ],
                [
                    InlineKeyboardButton("قـناه السـورس", url="https://t.me/PX_CBL")
                ],
                [
                    InlineKeyboardButton("اضغط لاضافتي لمجموعتك⚡", url=f"https://t.me/{app.username}?startgroup=true")
                ]
            ]
        )
    )

# ⬇️ دالة لجلب معلومات المطور
async def get_developer_info(client: Client, message: Message, username: str, title: str):
    try:
        usr = await client.get_chat(username)  # جلب معلومات المستخدم
        name = usr.first_name
        username_text = f"@{usr.username}" if usr.username else "لا يوجد"
        user_id = f"`{usr.id}`"
        bio = usr.bio if usr.bio else "لا توجد معلومات متاحة"
        
        # التحقق مما إذا كان لدى المستخدم صورة شخصية
        if usr.photo:
            photo_path = await client.download_media(usr.photo.big_file_id)
            await message.reply_photo(
                photo_path,
                caption=f"⍟ {title} ⍟\n\n"
                        f"✦ الاسم: {name}\n"
                        f"✦ المعرف: {username_text}\n"
                        f"✦ الايـدي: {user_id}\n"
                        f"✦ الـبايو: {bio}\n\n"
                        f"⍟ ســورس ميــوزك Titanx ⍟",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(name, url=f"https://t.me/{usr.username}")]]),
            )
        else:
            await message.reply(
                f"⍟ {title} ⍟\n\n"
                f"✦ الاسم: {name}\n"
                f"✦ المعرف: {username_text}\n"
                f"✦ الايـدي: {user_id}\n"
                f"✦ الـبايو: {bio}\n\n"
                f"⍟ ســورس ميــوزك Titanx ⍟",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(name, url=f"https://t.me/{usr.username}")]]),
            )
    except Exception as e:
        await message.reply(f"⚠️ حدث خطأ أثناء جلب المعلومات:\n`{str(e)}`")

# ⬇️ أمر لجلب معلومات "المطور فوكس"
@app.on_message(filters.command(["المطور فوكس", "🦊", "فوكس", "مبرمج السورس"]))
async def show_developer_info(client: Client, message: Message):
    await get_developer_info(client, message, "Fox4566", "معلومات مبرمج السورس")

# ⬇️ أمر لجلب معلومات "مطور السورس" (Loo_la3)
@app.on_message(filters.command(["مطور السورس", "alaa", "بودا"]))
async def show_programmer_info_ahmed(client: Client, message: Message):
    await get_developer_info(client, message, "Loo_la3", "معلومات مبرمج السورس")

# تأكد من تشغيل التطبيق
async def main():
    await app.start()

loop = asyncio.get_event_loop()
if loop.is_running():
    asyncio.create_task(main())
else:
    loop.run_until_complete(main())

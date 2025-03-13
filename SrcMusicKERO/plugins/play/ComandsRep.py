import sys
import asyncio
import requests
import re
import string
from pyrogram.types import Message
from pyrogram import filters, Client
from pyrogram.types import (InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup)
from SrcMusicKERO import app

# استارت
@app.on_message(filters.command(["الاوامر"], ""))
async def italy(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://envs.sh/S7N.webp",
        caption=f"""*مرحبًا {message.from_user.mention} 🌟*

أهلاً بك في **سورس Titanx** الرائع! إليك قائمة الأوامر التي يمكنك استخدامها:

📝 **أوامر المجموعات**:
- لتشغيل الأغاني: *تشغيل* أو *شغل* 🎶
- لتشغيل الفيديو: *فيديو* 🎥
- لإيقاف الأغنية الحالية: *ايقاف* أو *انهاء* ⏸️
- لتخطي الأغنية: *تخطي* ⏩

🔧 **أوامر القنوات**:
- لتشغيل الأغاني في القناة: *تشغيل* أو *شغل* 🎧
- لإيقاف الأغنية في القناة: *ايقاف* أو *انهاء* 🚫

🤖 **أوامر البوت**:
- لعرض إحصائيات البوت: *الإحصائيات* 📊
- للتحكم في لغة البوت: *اللغة* 🌐

🌟 **مميزات السورس**:
- لعرض كليشة السورس: *سورس* 💡
- لعرض معلومات عن البوت: *بوت* 🤖

🔒 **أوامر أخرى**:
- لتغيير الإعدادات: *الإعدادات* ⚙️
- لمعرفة معلومات شخص: *كشف* 🕵️‍♂️

▰▰▰▰▰▰▰▰▰▰▰▰▰
اضغط على الأزرار أدناه لاختيار المزيد من الخيارات 📲""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "أوامر المجموعات 🏠", callback_data=f"italygro"),
                    InlineKeyboardButton(
                        "أوامر القنوات 📡", callback_data=f"italycha"),
                ],
                [
                    InlineKeyboardButton(
                        "أوامر البوت 🤖", callback_data=f"italybot"),
                ],
                [
                    InlineKeyboardButton(
                        "مميزات السورس 💎", callback_data=f"italysou"),
                ],
                [
                    InlineKeyboardButton(
                        "مطور البرنامج 👨‍💻", callback_data=f"italydev"),
                ],
                [
                    InlineKeyboardButton(
                        "إغلاق ❌", callback_data=f"close"),
                ],
            ]
        ),
    )

# كول باك أوامر المجموعه
@app.on_callback_query(filters.regex("italygro"))
async def italy(_, query: CallbackQuery):
   await query.edit_message_caption(caption=f"""✅ **اليك قائمة أوامر المجموعات ♬**
❅─────✧❅✦❅✧─────❅
▰▰▰▰▰▰▰▰▰▰▰▰
- لتشغيل أغنية اكتب: *تشغيل* أو *شغل* 🎶
- لتشغيل فيديو اكتب: *فيديو* 🎥
- لإنهاء الأغنية اكتب: *ايقاف* أو *انهاء* ⏸️
- لتخطي الأغنية اكتب: *تخطي* ⏩
- إذا حدث خطأ أو لإعادة التشغيل اكتب: */restart* 🔄
▰▰▰▰▰▰▰▰▰▰▰▰
❅─────✧❅✦❅✧─────❅""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "أوامر القنوات 📡", callback_data=f"italycha"),
                    InlineKeyboardButton(
                        "أوامر البوت 🤖", callback_data=f"italybot"),
                ],
                [
                    InlineKeyboardButton(
                        "مميزات السورس 💎", callback_data=f"italysou"),
                ],
                [
                    InlineKeyboardButton(
                        "مطور البرنامج 👨‍💻", callback_data=f"italydev"),
                ],
                [
                    InlineKeyboardButton(
                        "إغلاق ❌", callback_data=f"close"),
                ],
            ]
        ),
    )

# كول باك أوامر القناه
@app.on_callback_query(filters.regex("italycha"))
async def italy(_, query: CallbackQuery):
   await query.edit_message_caption(caption=f"""✅ **اليك قائمة أوامر القنوات ♬**
▰▰▰▰▰▰▰▰▰▰▰▰
- لتشغيل أغنية اكتب: *تشغيل* أو *شغل* 🎶
- لتشغيل فيديو اكتب: *فيديو* 🎥
- لإنهاء الأغنية اكتب: *ايقاف* أو *انهاء* ⏸️
- لتخطي الأغنية اكتب: *تخطي* ⏩
- إذا حدث خطأ أو لإعادة التشغيل اكتب: */restart* 🔄
▰▰▰▰▰▰▰▰▰▰▰▰""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "أوامر المجموعات 🏠", callback_data=f"italygro"),
                    InlineKeyboardButton(
                        "أوامر البوت 🤖", callback_data=f"italybot"),
                ],
                [
                    InlineKeyboardButton(
                        "مميزات السورس 💎", callback_data=f"italysou"),
                ],
                [
                    InlineKeyboardButton(
                        "مطور البرنامج 👨‍💻", callback_data=f"italydev"),
                ],
                [
                    InlineKeyboardButton(
                        "إغلاق ❌", callback_data=f"close"),
                ],
            ]
        ),
    )

# كول باك أوامر البوت
@app.on_callback_query(filters.regex("italybot"))
async def italy(_, query: CallbackQuery):
   await query.edit_message_caption(caption=f"""✅ **اليك قائمة أوامر البوت ♬**
▰▰▰▰▰▰▰▰▰▰▰▰
- لعمل إذاعة في البوت: *إذاعة* 📢
- لعرض إحصائيات البوت: *الإحصائيات* 📊
- لعرض سرعة البوت: *بينج* ⏱️
- للتحكم في لغة البوت: *اللغة* 🌐
- للتحكم في إعدادات التشغيل: *الإعدادات* ⚙️
- لأوامر الحظر والرفع في كيبورد المطور
▰▰▰▰▰▰▰▰▰▰▰▰""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "أوامر المجموعات 🏠", callback_data=f"italygro"),
                    InlineKeyboardButton(
                        "أوامر القنوات 📡", callback_data=f"italycha"),
                ],
                [
                    InlineKeyboardButton(
                        "مميزات السورس 💎", callback_data=f"italysou"),
                ],
                [
                    InlineKeyboardButton(
                        "مطور البرنامج 👨‍💻", callback_data=f"italydev"),
                ],
                [
                    InlineKeyboardButton(
                        "إغلاق ❌", callback_data=f"close"),
                ],
            ]
        ),
    )

# كول باك أوامر مميزات السورس
@app.on_callback_query(filters.regex("italysou"))
async def italy(_, query: CallbackQuery):
   await query.edit_message_caption(caption=f"""✅ **اليك قائمة مميزات سورس Titanx ♬**
▰▰▰▰▰▰▰▰▰▰▰▰
- لعرض كليشة السورس: *سورس* 💡
- لعرض مين في الكول: *مين في الكول* 🧑‍🤝‍🧑
- لزخرفة النصوص: *زخرفه* ✨
- لعرض بوت الحذف: *بوت حذف* 🗑️
- لصناعة رابط تليجراف: *تليجراف* 🌐
- لتحويل الملصق لصورة: *Pict* 🖼️
- لتحويل الصورة لملصق: *Stik* 🏷️
▰▰▰▰▰▰▰▰▰▰▰▰
❅─────✧❅✦❅✧─────❅""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("أوامر المجموعات 🏠", callback_data="italygro"),
                    InlineKeyboardButton("أوامر القنوات 📡", callback_data="italycha"),
                ],
                [
                    InlineKeyboardButton("أوامر البوت 🤖", callback_data="italybot"),
                ],
                [
                    InlineKeyboardButton("مطور البرنامج 👨‍💻", callback_data="italydev"),
                ],
                [
                    InlineKeyboardButton("إغلاق ❌", callback_data="close"),
                ],
            ]
        ),
    )

# كول باك مطور البرنامج
@app.on_callback_query(filters.regex("italydev"))
async def italy(_, query: CallbackQuery):
   await query.edit_message_caption(caption=f"""✅ **مطور البرنامج:**
▰▰▰▰▰▰▰▰▰▰▰▰
- المطور: **@F_o_x_5** 🧑‍💻
- الدعم الفني: **@Support_Channel** 📩
- لمزيد من المعلومات، تواصل مع المطور مباشرة! 📬
▰▰▰▰▰▰▰▰▰▰▰▰
❅─────✧❅✦❅✧─────❅""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("أوامر المجموعات 🏠", callback_data="italygro"),
                    InlineKeyboardButton("أوامر القنوات 📡", callback_data="italycha"),
                ],
                [
                    InlineKeyboardButton("أوامر البوت 🤖", callback_data="italybot"),
                ],
                [
                    InlineKeyboardButton("مميزات السورس 💎", callback_data="italysou"),
                ],
                [
                    InlineKeyboardButton("إغلاق ❌", callback_data="close"),
                ],
            ]
        ),
    )

# كول باك إغلاق
@app.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()

# تشغيل البوت
if __name__ == "__main__":
    app.run()

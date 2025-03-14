from datetime import datetime
import random

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message, User
from SrcMusicKERO.plugins.play.filters import command
from SrcMusicKERO import app


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


# رسالة معلومات المستخدم مع الثيمات
infotext = (
    "◂  **معلومات المستخدم** 🦊\n"
    "⩹⌯⊷━♢ ⦓ Titanx ⦔ ♢━⊶⌯⩺\n"
    "✯ **الاسم الكامل** ➠ [{full_name}](tg://user?id={user_id}) 🦊\n"
    "✯ **معرف المستخدم** ➠ `{user_id}` 🦊\n"
    "✯ **الاسم الأول** ➠ `{first_name}` 🦊\n"
    "✯ **الاسم الأخير** ➠ `{last_name}` 🦊\n"
    "✯ **اسم المستخدم** ➠ `@{username}` 🦊\n"
    "✯ **آخر ظهور** ➠ `{last_online}` 🦊\n"
    "✯ **السيرة الذاتية** ➠ `{bio}` 🦊\n"
    "⩹⌯⊷━♢ ⦓ Titanx ⦔ ♢━⊶⌯⩺"
)


# دالة لمعرفة الحالة الأخيرة للمستخدم
def LastOnline(user: User):
    if user.is_bot:
        return "بوت"
    elif user.status == "recently":
        return "مؤخرًا"
    elif user.status == "within_week":
        return "في الأسبوع الماضي"
    elif user.status == "within_month":
        return "في الشهر الماضي"
    elif user.status == "long_time_ago":
        return "منذ وقت طويل"
    elif user.status == "online":
        return "متصل حاليًا"
    elif user.status == "offline":
        return datetime.fromtimestamp(user.status.date).strftime(
            "%a, %d %b %Y, %H:%M:%S"
        )


# دالة للحصول على الاسم الكامل للمستخدم
def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


# دالة لتحديد مستوى التفاعل وإرسال رسالة عشوائية
def get_user_interaction(user_id: int):
    # هنا نضع طرقًا لتحديد تفاعل المستخدم مثل عدد الرسائل أو نشاطه
    interactions = {
        "low": [
            " شيد حيلك يانجم عاوز افتخر بيك😒",
            "اي ينجم متخلينا نفرح بيك واتاخد ادمن 🥲"
        ],
        "medium": [
            "ايو يحب سامع انك نايم عندنا في بار  انا هديك قلبي ❤️‍🔥",
            " العضو بتاعي  اهو 👑 اهو اهو "
        ],
        "high": [
            "مبروك يقلب اخوك او اخوكي انتي او انتا  هتاخد رول وقلبي قريبنا لتفعلك النار 💃💃💃💃",
            "تفاعلك نار وشرار🔥🔥🔥"
        ]
    }

    # هنا نحدد تفاعل المستخدم بناءً على رقم عشوائي، ويمكنك تخصيص ذلك بناءً على البيانات الحقيقية
    interaction_level = random.choice(["low", "medium", "high"])
    return random.choice(interactions[interaction_level])


@app.on_message(command("كشف"))
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("لا أعرف هذا المستخدم.")
        return
    desc = await client.get_chat(get_user)
    desc = desc.description

    # احصل على مستوى التفاعل مع المستخدم وأرسل رسالة عشوائية
    interaction_message = get_user_interaction(user.id)

    await message.reply_text(
        infotext.format(
            full_name=FullName(user),
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name if user.last_name else "",
            username=user.username if user.username else "",
            last_online=LastOnline(user),
            bio=desc if desc else "`فارغ.`",
        ),
        disable_web_page_preview=True,
    )
    
    # إرسال رسالة عشوائية بناءً على تفاعل المستخدم
    await message.reply(interaction_message)

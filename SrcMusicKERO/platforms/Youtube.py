import asyncio
import re
from typing import Union
import yt_dlp
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardMarkup
from youtubesearchpython.__future__ import VideosSearch

from SrcMusicKERO import app
from SrcMusicKERO.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
)
from SrcMusicKERO.utils.inline import botplaylist_markup
from config import PLAYLIST_IMG_URL, SUDOERS, adminlist
from strings import get_string

# 🔹 مسار ملف الكوكيز
cookies_file = "/fox2/cookies/cookies_fixed.txt"

# 🔹 تخزين روابط الدعوات لتسريع الانضمام
links = {}

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.listbase = "https://youtube.com/playlist?list="
        self.regex = r"(?:youtube\.com|youtu\.be)"

    async def url(self, message):
        """ استخراج رابط الفيديو من الرسالة أو البحث عنه """
        text = message.text or message.caption  
        if not text:
            return None

        # البحث عن رابط يوتيوب داخل الرسالة
        url_match = re.search(
            r"(https?://)?(www\.)?"
            r"(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)"
            r"([\w-]+)", text
        )

        if url_match:
            return "https://www.youtube.com/watch?v=" + url_match.group(4)

        # البحث عن الفيديو إذا لم يتم إدخال رابط
        query = " ".join(text.split()[1:])  # حذف أول كلمة (الأمر نفسه مثل "تشغيل")
        if not query:
            return None  # إذا لم يتم إدخال أي اسم، لا تفعل شيئًا

        print(f"🔎 البحث عن: {query}")
        search = VideosSearch(query, limit=1)
        results = await search.next()
        
        if results["result"]:
            video_url = results["result"][0]["link"]
            print(f"✅ تم العثور على الفيديو: {video_url}")
            return video_url
        else:
            print("❌ لم يتم العثور على أي نتائج!")
            return None

    async def video(self, link):
        """ جلب رابط الفيديو باستخدام yt-dlp """
        print(f"🔹 تشغيل video() مع الرابط: {link}")
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", cookies_file,
            "-g",
            "-f",
            "bestaudio",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return (1, stdout.decode().split("\n")[0]) if stdout else (0, stderr.decode())


# 🔹 تغليف أوامر التشغيل
def PlayWrapper(command):
    async def wrapper(client, message):
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        try:
            await message.delete()
        except:
            pass

        youtube = YouTubeAPI()
        url = await youtube.url(message)

        if not url:
            return await message.reply_text("❌ لم يتم العثور على فيديو!")

        chat_id = await get_cmode(message.chat.id) if message.command[0][0] == "c" else message.chat.id
        channel = None if chat_id == message.chat.id else (await app.get_chat(chat_id)).title

        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)

        if playty != "Everyone" and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id, [])
            if message.from_user.id not in admins:
                return await message.reply_text(_["admin_13"] if not admins else _["play_4"])

        video = "v" in message.command[0] or "-v" in message.text
        fplay = message.command[0][-1] == "e"

        if not await is_active_chat(chat_id):
            userbot = await get_assistant(chat_id)
            try:
                get = await app.get_chat_member(chat_id, userbot.id)
                if get.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
                    return await message.reply_text(_["call_2"].format(app.mention, userbot.id, userbot.name, userbot.username))
            except ChatAdminRequired:
                return await message.reply_text(_["call_1"])

        try:
            await app.get_chat_member(chat_id, userbot.id)
        except UserNotParticipant:
            invitelink = links.get(chat_id) or await get_invite_link(message, chat_id, userbot)
            await handle_invite_and_join(message, chat_id, userbot, invitelink)

        return await command(client, message, _, chat_id, video, channel, playmode, url, fplay)

    return wrapper


async def get_invite_link(message, chat_id, userbot):
    try:
        invitelink = message.chat.username or await app.export_chat_invite_link(chat_id)
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
        return invitelink
    except ChatAdminRequired:
        return await message.reply_text("❌ البوت لا يملك صلاحية إنشاء روابط دعوة.")
    except Exception as e:
        return await message.reply_text(f"⚠️ خطأ أثناء استخراج رابط الدعوة: {type(e).__name__}")


async def handle_invite_and_join(message, chat_id, userbot, invitelink):
    myu = await message.reply_text("🔄 محاولة انضمام البوت...")
    try:
        await asyncio.sleep(1)
        await userbot.join_chat(invitelink)
    except InviteRequestSent:
        try:
            await app.approve_chat_join_request(chat_id, userbot.id)
            await asyncio.sleep(3)
            await myu.edit("✅ تم قبول طلب الانضمام بنجاح.")
        except Exception as e:
            return await message.reply_text(f"❌ فشل قبول طلب الانضمام: {type(e).__name__}")
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        return await message.reply_text(f"⚠️ فشل الانضمام: {type(e).__name__}")

    links[chat_id] = invitelink
    try:
        await userbot.resolve_peer(chat_id)
    except:
        pass

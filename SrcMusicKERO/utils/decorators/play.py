import asyncio
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SrcMusicKERO import YouTube, app
from SrcMusicKERO.misc import SUDOERS
from SrcMusicKERO.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_maintenance,
)
from SrcMusicKERO.utils.inline import botplaylist_markup
from config import PLAYLIST_IMG_URL, SUPPORT_CHAT, adminlist
from strings import get_string

links = {}

# دالة لتغليف أوامر التشغيل
def PlayWrapper(command):
    async def wrapper(client, message):
        # الحصول على اللغة واختيار الترجمة
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        # التحقق من حالة الصيانة
        if await is_maintenance() is False and message.from_user.id not in SUDOERS:
            return await message.reply_text(
                text=f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a> ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                disable_web_page_preview=True,
            )

        # محاولة حذف الرسالة
        try:
            await message.delete()
        except:
            pass

        # التحقق من المرفقات
        audio_telegram = message.reply_to_message.audio if message.reply_to_message else None
        video_telegram = message.reply_to_message.video if message.reply_to_message else None

        # محاولة الحصول على رابط الفيديو
        url = await YouTube.url(message)
        if not audio_telegram and not video_telegram and not url:
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text(_["str_1"])
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["play_18"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

        # تحديد معرّف الدردشة والمجموعة
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if not chat_id:
                return await message.reply_text(_["setting_7"])
            try:
                chat = await app.get_chat(chat_id)
            except:
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None

        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)

        # التحقق من الصلاحيات في حالة "playtype"
        if playty != "Everyone" and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins or message.from_user.id not in admins:
                return await message.reply_text(_["admin_13"] if not admins else _["play_4"])

        # تحديد ما إذا كان يجب تشغيل الفيديو أو الصوت
        video = True if message.command[0][0] == "v" or "-v" in message.text else False

        # التحقق من وضع التشغيل
        fplay = True if message.command[0][-1] == "e" else None

        # التحقق من النشاط في الدردشة
        if not await is_active_chat(chat_id):
            userbot = await get_assistant(chat_id)
            try:
                get = await app.get_chat_member(chat_id, userbot.id)
            except ChatAdminRequired:
                return await message.reply_text(_["call_1"])

            # التحقق من الحظر
            if get.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
                return await message.reply_text(
                    _["call_2"].format(app.mention, userbot.id, userbot.name, userbot.username)
                )

        # التحقق من عضوية البوت في الدردشة
        try:
            await app.get_chat_member(chat_id, userbot.id)
        except UserNotParticipant:
            if chat_id in links:
                invitelink = links[chat_id]
            else:
                invitelink = await get_invite_link(message, chat_id, userbot)

            # الانضمام إلى الدردشة إذا لم يكن العضو موجودًا
            await handle_invite_and_join(message, chat_id, userbot, invitelink)

        # استدعاء الدالة الأصلية مع جميع المعاملات
        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper


# دالة لاستدعاء رابط الدعوة
async def get_invite_link(message, chat_id, userbot):
    if message.chat.username:
        invitelink = message.chat.username
        try:
            await userbot.resolve_peer(invitelink)
        except:
            pass
    else:
        try:
            invitelink = await app.export_chat_invite_link(chat_id)
        except ChatAdminRequired:
            return await message.reply_text(_["call_1"])
        except Exception as e:
            return await message.reply_text(_["call_3"].format(app.mention, type(e).__name__))

    if invitelink.startswith("https://t.me/+"):
        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
    return invitelink


# دالة لمعالجة الدعوة والانضمام
async def handle_invite_and_join(message, chat_id, userbot, invitelink):
    myu = await message.reply_text(_["call_4"].format(app.mention))
    try:
        await asyncio.sleep(1)
        await userbot.join_chat(invitelink)
    except InviteRequestSent:
        try:
            await app.approve_chat_join_request(chat_id, userbot.id)
        except Exception as e:
            return await message.reply_text(_["call_3"].format(app.mention, type(e).__name__))
        await asyncio.sleep(3)
        await myu.edit(_["call_5"].format(app.mention))
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        return await message.reply_text(_["call_3"].format(app.mention, type(e).__name__))

    links[chat_id] = invitelink
    try:
        await userbot.resolve_peer(chat_id)
    except:
        pass

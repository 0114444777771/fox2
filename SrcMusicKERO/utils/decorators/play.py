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
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        # تعديل شرط الصيانة إلى False بدلاً من تعطيله
        if await is_maintenance() == False or message.from_user.id in SUDOERS:
            pass
        else:
            return await message.reply_text(
                text=f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a> ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                disable_web_page_preview=True,
            )

        try:
            await message.delete()
        except:
            pass

        audio_telegram = message.reply_to_message.audio if message.reply_to_message else None
        video_telegram = message.reply_to_message.video if message.reply_to_message else None

        url = await YouTube.url(message) if hasattr(YouTube, "url") else None

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

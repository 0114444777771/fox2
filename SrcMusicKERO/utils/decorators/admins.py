from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from SrcMusicKERO import app
from SrcMusicKERO.misc import SUDOERS, db
from SrcMusicKERO.utils.database import (
    get_authuser_names,
    get_cmode,
    get_lang,
    get_upvote_count,
    is_active_chat,
    is_maintenance,
    is_nonadmin_chat,
    is_skipmode,
)
from config import adminlist, confirmer
from strings import get_string  # ✅ استيراد صحيح

from ..formatters import int_to_alpha


def AdminRightsCheck(mystic):
    async def wrapper(client, message):
        if await is_maintenance() is False:
            if message.from_user and message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ.",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        try:
            language = await get_lang(message.chat.id) or "en"
            _ = get_string(language)  # ✅ استدعاء صحيح
        except:
            _ = get_string("en")

        chat_id = await get_cmode(message.chat.id) if message.command[0][0] == "c" else message.chat.id

        if not await is_active_chat(chat_id):
            return await message.reply_text(_["general_5"])

        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin and message.from_user and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins or message.from_user.id not in admins:
                return await message.reply_text(_["admin_14"])

        return await mystic(client, message, _, chat_id)

    return wrapper


def AdminActual(mystic):
    async def wrapper(client, message):
        if await is_maintenance() is False:
            if message.from_user and message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ.",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        try:
            language = await get_lang(message.chat.id) or "en"
            _ = get_string(language)
        except:
            _ = get_string("en")

        if message.from_user.id and message.from_user.id not in SUDOERS:
            try:
                member = (await app.get_chat_member(message.chat.id, message.from_user.id)).privileges
            except:
                return
            if not member.can_manage_video_chats:
                return await message.reply(_["general_4"])

        return await mystic(client, message, _)

    return wrapper


def ActualAdminCB(mystic):
    async def wrapper(client, CallbackQuery):
        if await is_maintenance() is False:
            if CallbackQuery.from_user.id not in SUDOERS:
                return await CallbackQuery.answer(
                    f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ.",
                    show_alert=True,
                )

        try:
            language = await get_lang(CallbackQuery.message.chat.id) or "en"
            _ = get_string(language)
        except:
            _ = get_string("en")

        if CallbackQuery.message.chat.type == ChatType.PRIVATE:
            return await mystic(client, CallbackQuery, _)

        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            try:
                a = (await app.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)).privileges
            except:
                return await CallbackQuery.answer(_["general_4"], show_alert=True)
            if not a.can_manage_video_chats and CallbackQuery.from_user.id not in SUDOERS:
                token = await int_to_alpha(CallbackQuery.from_user.id)
                _check = await get_authuser_names(CallbackQuery.from_user.id)
                if token not in _check:
                    return await CallbackQuery.answer(_["general_4"], show_alert=True)

        return await mystic(client, CallbackQuery, _)

    return wrapper

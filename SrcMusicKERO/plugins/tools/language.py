from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message

from SrcMusicKERO import app
from SrcMusicKERO.utils.database import get_lang, set_lang
from SrcMusicKERO.utils.decorators import ActualAdminCB, language, languageCB
from config import BANNED_USERS
from strings import get_string, languages_present


def languages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        *[
            InlineKeyboardButton(
                text=languages_present[i],
                callback_data=f"languages:{i}",
            )
            for i in languages_present
        ]
    )
    keyboard.row(
        InlineKeyboardButton(
            text="🌍 اختيار اللغة",
            callback_data="change_lang",
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settingsback_helper",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
    )
    return keyboard


@app.on_message(filters.command(["lang", "setlang", "language"]) & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    keyboard = languages_keyboard(_)
    await message.reply_text(
        _["lang_1"],
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def language_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = languages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    language = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    if str(old) == str(language):
        return await CallbackQuery.answer(_["lang_4"], show_alert=True)
    try:
        _ = get_string(language)
        await CallbackQuery.answer(_["lang_2"], show_alert=True)
    except:
        _ = get_string(old)
        return await CallbackQuery.answer(
            _["lang_3"],
            show_alert=True,
        )
    await set_lang(CallbackQuery.message.chat.id, language)
    keyboard = languages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


# زر اختيار اللغة
@app.on_callback_query(filters.regex("change_lang") & ~BANNED_USERS)
@languageCB
async def change_language_callback(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = languages_keyboard(_)
    await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)

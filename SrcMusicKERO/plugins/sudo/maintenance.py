from SrcMusicKERO.plugins.play.filters import command
from pyrogram import filters
from pyrogram.types import Message

from SrcMusicKERO import app
from SrcMusicKERO.misc import SUDOERS
from SrcMusicKERO.utils.database import (
    get_lang,
    is_maintenance,
    maintenance_off,
    maintenance_on,
)
from strings import get_string


@app.on_message(command(["الصيانه", "/maintenance"]) & SUDOERS)
async def maintenance(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
    usage = _["maint_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "تفعيل":
        if await is_maintenance() is False:
            await message.reply_text(_["maint_4"])
        else:
            await maintenance_off()
            await message.reply_text(_["maint_2"].format(app.mention))
    elif state == "تعطيل":
        if await is_maintenance() is False:
            await maintenance_off()
            await message.reply_text(_["maint_3"].format(app.mention))
        else:
            await message.reply_text(_["maint_5"])
    else:
        await message.reply_text(usage)

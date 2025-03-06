from pyrogram.enums import ParseMode

from SrcMusicKERO import app
from SrcMusicKERO.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
ٴ<b>•────‌‌‏──‌‌‏─‌‌‏─‌‌‏─‌‌‏─‌‌‏─‌‌‏─•</b>
<b>Music NoTiFiCaTiOnS 𝄞</b>
ٴ<b>•────‌‌‏─‌‌‏─‌‌‏─‌‌‏─‌‌‏──‌‌‏─‌‌‏─•</b>
<b>- My PrOgRam💸</b>
<b>- There is someone currently using Music🎻ً</b>

<b>- NaMe🎭 :</b> {message.from_user.mention}
<b>- UsEr🐊 :</b> @{message.from_user.username}
<b>- Id 🐼 :</b> <code>{message.from_user.id}</code>

<b>- NaMe GrOuP👥 :</b> {message.chat.title}
<b>- UsE GrOuP👀 :</b> @{message.chat.username}
<b>- Id GrOuP🦠 :</b> <code>{message.chat.id}</code>

<b>- QuErY🌐 :</b> {message.text.split(None, 1)[1]}
<b>- StReMaTyPe🎯 :</b> {streamtype}"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return

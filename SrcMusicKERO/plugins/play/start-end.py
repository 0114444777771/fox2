import asyncio
from pyrogram import Client, filters
from strings.filters import command
from pyrogram.types import *
from SrcMusicKERO import app

@app.on_message(filters.video_chat_started)
async def brah(client, message):
       await message.reply(" بدأت المحادثة الصوتية 👤")
@app.on_message(filters.video_chat_ended)
async def brah2(client, message):
    da = message.video_chat_ended.duration
    ma = divmod(da, 60)
    ho = divmod(ma[0], 60)
    day = divmod(ho[0], 24)
    if da < 60:
       await message.reply(f"تم انهاء مكالمة الفيديو مدتها {da} ثواني وصكرها ")        
    elif 60 < da < 3600:
        if 1 <= ma[0] < 2:
            await message.reply(f" تم انهاء مكالمة الفيديو مدتها دقيقه")
        elif 2 <= ma[0] < 3:
            await message.reply(f" تم انهاء مكالمة الفيديو مدتها دقيقتين ")
        elif 3 <= ma[0] < 11:
            await message.reply(f"تم انهاء مكالمة الفيديو مدتها {ma[0]} دقايق ")  
        else:
            await message.reply(f"تم إنهاء مكالمة الفيديو مدتها {ma[0]} دقيقه")
    elif 3600 < da < 86400:
        if 1 <= ho[0] < 2:
            await message.reply(f"تم انهاء مكالمة الفيديو مدتها ساعه ")
        elif 2 <= ho[0] < 3:
            await message.reply(f"تم انهاء مكالمة الفيديو مدتها ساعتين ")
        elif 3 <= ho[0] < 11:
            await message.reply(f"تم انهاء مكالمة الفيديو مدتها {ho[0]} ساعات ")  
        else:
            await message.reply(f"تم إنهاء مكالمة الفيديو مدتها {ho[0]} ساعة ")
    else:
        if 1 <= day[0] < 2:
            await message.reply(f"تم انهاء مكالمة الفيديو مدتها يوم ")
        elif 2 <= day[0] < 3:
            await message.reply(f" تم انهاء مكالمة الفيديو مدتها يومين ")
        elif 3 <= day[0] < 11:
            await message.reply(f" تم انهاء مكالمة الفيديو مدتها {day[0]} ايام ")  
        else:
            await message.reply(f" تم إنهاء مكالمة الفيديو مدتها {day[0]} يوم")

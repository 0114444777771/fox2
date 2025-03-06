import asyncio
import random
from SrcMusicKERO import app
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, Message)
from pyrogram import filters, Client
from SrcMusicKERO.plugins.play.filters import command




txt = [


"ها عايز اي 🙄",
"ايوااا جااااي 😂",
"عاوزني اشقطلك مين يروحي 🥺",
"ايوة قول عاوز اي 🤔",
"قلب البوت 🥺",
"بوت توب معاك يروحي🥺",
"استنا يعم بشقط وجايبك علطول 😂",

        ]


        


@app.on_message(command(["بوت","توب"]))

async def khyrok(client: Client, message: Message):

      a = random.choice(txt)

      await message.reply(

        f"{a}")

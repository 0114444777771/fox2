import asyncio

import os
import time
import requests
from config import START_IMG_URL
from pyrogram import filters
import random
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from strings.filters import command
from SrcMusicKERO import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from SrcMusicKERO import app
from random import  choice, randint

                
@app.on_message(
    command(["سورس","السورس"])
    
)
async def huhh(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://envs.sh/jUE.jpg",
        caption=f"""⍟ 𝚃𝙷𝙴 𝙱𝙴𝚂𝚃 𝚂𝙾𝚄𝚁𝙲𝙴 𝙾𝙽 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 ⍟""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "program", url=f"https://t.me/Fox4566"),
                 
             ],[ 
            InlineKeyboardButton(
                        "SouRce", url=f"https://t.me/Loo_la3"), 
                   
             ],[ 
                  InlineKeyboardButton(
                text="ADD Me For you Group",
                url=f"https://t.me/{app.username}?startgroup=true"),
                ],

            ]

        ),

    )






@app.on_message(command([" مطور السورس","فوكس","المطور"]))
async def yas(client, message):
    usr = await client.get_chat(" Fox4566")
    name = usr.first_name
    photo = await app.download_media(usr.photo.big_file_id)
    await message.reply_photo(photo,       caption=f"This Aliv Me Program.\n\n Name :{name}\n\n User :@{usr.username}\n\n Id :`{usr.id}`\n\n Bio :{usr.bio}\n\nSouRce Music Alex Best Source In Telegram", 
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        name, url=f"https://t.me/{usr.username}")
                ],
            ]
        ),
    )



@app.on_message(command(["جولينا" , "ALAA","بودا"]))
async def yas(client, message):
    usr = await client.get_chat("Loo_la3")
    name = usr.first_name
    photo = await app.download_media(usr.photo.big_file_id)
    await message.reply_photo(photo,       caption=f"This Alive Me Program.\n\n Name :{name}\n\n User :@{usr.username}\n\n ID :`{usr.id}`\n\n Bio:{usr.bio}\n\nSource Music Alex Best Source In Telegram", 
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        name, url=f"https://t.me/{usr.username}")
                ],
            ]
        ),
    )




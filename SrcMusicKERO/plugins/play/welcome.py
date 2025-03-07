import os
from pyrogram import Client, filters
from pyrogram.types import Message, User
from pyrogram import Client, emoji 
from SrcMusicKERO import app
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ChatPermissions
from SrcMusicKERO import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from pyrogram import filters


@app.on_message(filters.new_chat_members)
async def wel__come(client: Client, message: Message):
	chatid= message.chat.id
	await client.send_message(text=f"- نورت يا ياحلو 🌚♥ \n احترم الادمنيه ✨ \n تفاعل وخذ بوسه  {message.from_user.mention}\n│ \n└ʙʏ في {message.chat.title}",chat_id=chatid)
	
@app.on_message(filters.left_chat_member)
async def good_bye(client: Client, message: Message):
	chatid= message.chat.id
	await client.send_message(text=f"- يلا فدوه يا حبيبي لا تجي من جديد♥\n│ \n└ʙʏ  {message.from_user.mention} ",chat_id=chatid)
	
	
	
	
	
	
	
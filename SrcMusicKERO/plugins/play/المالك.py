import asyncio
import os
import time
import requests
from pyrogram import enums, filters, Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from SrcMusicKERO import app
from SrcMusicKERO.plugins.play.filters import command
from pyrogram.errors import FloodWait

# قائمة لتعطيل أو تفعيل أمر الايدي
iddof = []


@app.on_message(command(["المالك", "صاحب الخرابه", "المنشي"]), group=95)
async def ownner(client: Client, message: Message):
    x = [
        m.user.id async for m in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        ) if m.status == ChatMemberStatus.OWNER
    ]

    if not x:
        return await message.reply_text("عزيزي المالك هذا حساب محذوف\n༄")

    m = await app.get_users(x[0])

    if m.photo:
        photo = [p async for p in app.get_chat_photos(x[0], limit=1)][0]
        await message.reply_photo(
            photo.file_id,
            caption=f"<b>الاســم : {m.first_name}\n"
                    f"اســم المســتخدم : @{m.username}\n"
                    f"الايــدي : <code>{m.id}</code>\n"
                    f"الشــات : {message.chat.title}\n"
                    f"ايــدي الشــات : <code>{message.chat.id}</code></b>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(m.first_name, url=f"https://t.me/{m.username}")]]
            )
        )
    else:
        await message.reply_text(
            f"<b>الاســم : {m.first_name}\n"
            f"اســم المســتخدم : @{m.username}\n"
            f"الايــدي : <code>{m.id}</code>\n"
            f"الشــات : {message.chat.title}\n"
            f"ايــدي الشــات : <code>{message.chat.id}</code></b>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(m.first_name, url=f"https://t.me/{m.username}")]]
            )
        )


@app.on_message(command(["قفل الايدي", "تعطيل الايدي"]), group=2272)
async def iddlock(client, message):
    get = await client.get_chat_member(message.chat.id, message.from_user.id)
    if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        if message.chat.id in iddof:
            return await message.reply_text("تم معطل من قبل🔒")
        iddof.append(message.chat.id)
        return await message.reply_text("تم تعطيل الايدي بنجاح ✅🔒")
    else:
        return await message.reply_text("لازم تكون ادمن علشان تقدر تعطل الايدي")


@app.on_message(command(["فتح الايدي", "تفعيل الايدي"]), group=2292)
async def iddopen(client, message):
    get = await client.get_chat_member(message.chat.id, message.from_user.id)
    if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        if message.chat.id not in iddof:
            return await message.reply_text("الايدي مفعل من قبل ✅")
        iddof.remove(message.chat.id)
        return await message.reply_text("تم فتح الايدي بنجاح ✅🔓")
    else:
        return await message.reply_text("لازم تكون ادمن علشان تقدر تفعل الايدي")


@app.on_message(command(["ايدي", "الايدي", "ا"]), group=27722)
async def iddd(client, message):
    if message.chat.id in iddof:
        return

    usr = await client.get_chat(message.from_user.id)
    name = usr.first_name
    photo = None

    if usr.photo:
        async for p in app.get_chat_photos(message.from_user.id, limit=1):
            photo = p.file_id

    caption = (
        f"⤄ الاسم: {message.from_user.mention}\n"
        f"⤄ اليوزر: @{message.from_user.username}\n"
        f"⤄ الايدي: `{message.from_user.id}`\n"
        f"⤄ ʙɪᴏ: {usr.bio if usr.bio else 'لا يوجد'}\n"
        f"⤄ الجروب: {message.chat.title}\n"
        f"⤄ ايدي الجروب: `{message.chat.id}`"
    )

    if photo:
        await message.reply_photo(photo, caption=caption, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(name, url=f"https://t.me/{message.from_user.username}")]]
        ))
    else:
        await message.reply_text(caption, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(name, url=f"https://t.me/{message.from_user.username}")]]
        ))

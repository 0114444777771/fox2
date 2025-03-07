from pyrogram import Client, filters
from random import  choice, randint
from SrcMusicKERO import app
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InputMediaPhoto,
    Message,
)

@app.on_message(filters.command("تخ", [".", ""]) & filters.group & filters.reply)
async def huhh(client, message):
    user = message.from_user
    await message.reply_animation(
        animation="https://telegra.ph/file/b90d4b29a715fb542544a.mp4",
        caption=f"""≭︰هذا الشخص القاتل🧟 ⦗ {message.from_user.mention} ⦘\n≭︰هذا الشخص المقتول🥀 ↫ ⦗ {message.reply_to_message.from_user.mention} ⦘\nانا لله وانـا اليـه راجعـون """,
        reply_markup=InlineKeyboardMarkup(
            [
               [
                   InlineKeyboardButton(
                       "المقتول 🔪", url=f"https://t.me/{message.reply_to_message.from_user.username}"
                   )],[
               ],
           ]
        )
    )
    

@app.on_message(filters.command("تف", [".", ""]) & filters.group & filters.reply)
async def huhh(client, message):
    user = message.from_user
    await message.reply_animation(
        animation="https://telegra.ph/file/4a1f6a9bacb1a863f03f1.mp4",
        caption=f"""≭︰هذا هو التافف🤢 ⦗ {message.from_user.mention} ⦘\n≭︰المتفوف عليه 😢 ↫ ⦗ {message.reply_to_message.from_user.mention} ⦘\nجاتكوك القرف يعيال يمقرفه """,
        reply_markup=InlineKeyboardMarkup(
            [
               [
                   InlineKeyboardButton(
                       "المجني عليه 😢", url=f"https://t.me/{message.reply_to_message.from_user.username}"
                  )],[
               ],
           ]
        )
    )


@app.on_message(filters.command("مح", [".", ""]) & filters.group & filters.reply)
async def huhh(client, message):
    user = message.from_user
    await message.reply_animation(
        animation="https://telegra.ph/file/3dd136786231ab017bd53.mp4",
        caption=f"""الممحون اللي باعت بوسه 🥺↫ ⦗ {message.from_user.mention} ⦘\nمبعوتلك البوسه يملبن انت 🤤 ↫ ⦗ {message.reply_to_message.from_user.mention} ⦘\n اي المحن دا يولاد جوزوني بقي 🥺""",
        reply_markup=InlineKeyboardMarkup(
            [
               [
                   InlineKeyboardButton(
                       "المتباس 💋", url=f"https://t.me/{message.reply_to_message.from_user.username}"
                   )],[
               ],
           ]
        )
    )
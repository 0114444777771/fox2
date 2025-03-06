from pyrogram import Client
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from SrcMusicKERO import app
import os


@app.on_chat_member_updated(filters=lambda _, response: response.new_chat_member, group=847)
async def WelcomeDev(_, response: ChatMemberUpdated):
    dev_id = 7020374464# حط ايديك هنا
    if response.from_user.id == dev_id:
        info = await app.get_chat(dev_id)
        name = info.first_name
        bio = info.bio
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(name, user_id=dev_id)]
        ])
        await app.download_media(info.photo.big_file_id, file_name=os.path.join("downloads", "developer.jpg"))
        await app.send_photo(
            chat_id=response.chat.id,
            reply_markup=markup,
            photo="downloads/developer.jpg", 
            caption=f" دخل الشات المبرمج احمد يجب ع كل الاعضاء احترامه وتقديره ☘️🤍 \n{name} \n- {bio}"
        )

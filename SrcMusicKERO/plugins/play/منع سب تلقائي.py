from pyrogram import Client
from pyrogram import filters
from SrcMusicKERO import app

#منع الكلام السيئ
@app.on_message(filters.text)
async def delete_text(client, message):
    word_list = ["سكس", "منتاك","عرص","خول","شرموط","يبن الشرموطه","يبن المتناكه","يبن الاحبه","ينعل كسمك","كسمك"]
    if message.text in word_list:
        await client.delete_messages(message.chat.id, message.id)
        await client.send_message(message.chat.id, f"لا تسب يابن المتناكه {message.from_user.first_name}")
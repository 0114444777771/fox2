import asyncio
from pyrogram import Client, filters
from strings.filters import command
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from SrcMusicKERO import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)



REPLY_MESSAGE = "صلي علي اشرف خلق الله🌚🌺"

REPLY_MESSAGE_BUTTONS = [
    [
        ("الاوامر"),
    ],
    [

            (" غنيلي "),                   

             (" متحركه ")

          ],

          [

             (" مبرمج السورس ")

          ],

          [
              
             ("━━━━━━━━━━━━"),
              
          ],

          [
              
              (" اقتباس "),                   

             (" كت تويت ")
              
          ],

          [ 
              
              (" فيلم "),                   

             (" صراحه ")

          ],

          [
              
             ("━━━━━━━━━━━━"),
              
          ],

          [ 

             (" انمي "),

             (" صور ")

          ],

          [

             (" استوري "),

             (" السورس ")

          ],

          [
              
             ("━━━━━━━━━━━━"),

          ],

          [

             (" هيدرات "),
       
               (" قران "), 
          ], 

          [
       
           ("❎ ¦ حذف الكيبورد")
    ]
]

@app.on_message(filters.regex("^/RED"), group=39)
async def cpanel(_, message: Message):             
        text = REPLY_MESSAGE
        reply_markup = ReplyKeyboardMarkup(REPLY_MESSAGE_BUTTONS, resize_keyboard=True, selective=True)
        await message.reply(
              text=text,
              reply_markup=reply_markup
        )


@app.on_message(filters.command(["❎ ¦ حذف الكيبورد"], ""))
async def upbkgt(client: Client, message: Message):
    await message.reply_text(
        text="""❎ ¦ تم حذف الكيبورد بنجاح""",
        reply_markup=ReplyKeyboardRemove()
    )
@app.on_message(filters.regex("يـوتيوب. 📽"))
def reply_to_HEY(Client, message):
    message.reply_video(
        video=f"https://telegra.ph/file/9a8329cc7b5fc2df92a2f.mp4",
        caption=f"""يتم استخدام هذا الامر لعرض تحميل من اليوتيوب\nاستخدم الامر بهذا الشكل `تنزيل`  او  `يوتيوب`  كمثل تنزيل سوره الرحمن اضغط علي الامر لنسخ والاستخدا """,
        reply_markup=InlineKeyboardMarkup(
            [
            [
              InlineKeyboardButton("مبرمج السورس", url=f"https://t.me/U_H_D8"),
            ]
         ]
     )
  )




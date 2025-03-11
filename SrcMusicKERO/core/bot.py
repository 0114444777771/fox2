from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Zelzaly(Client):
    def __init__(self):
        LOGGER("ميوزك الــيكـس").info("جارِ بدء تشغيل البوت . . .")
        super().__init__(
            name="SrcMusicKERO",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()  # تحميل بيانات البوت بشكل صحيح
        self.id = me.id
        self.name = me.first_name + " " + (me.last_name or "")
        self.username = me.username
        self.mention = me.mention

        # التحقق من LOGGER_ID
        if not config.LOGGER_ID:
            LOGGER(__name__).error("» خطأ: لم يتم تعيين معرف مجموعة السجل (LOGGER_ID) في config.py.")
            exit()

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» تم تشغيل الميـوزك لـ البوت {self.mention} :</b></u>\n\n"
                     f"- ɪᴅ : <code>{self.id}</code>\n"
                     f"- ɴᴀᴍᴇ : {self.name}\n"
                     f"- ᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error("» قم باضافة البـوت مشـرفـاً بكافة الصلاحيات في مجموعـة السجـل")
            exit()
        except Exception as ex:
            LOGGER(__name__).error(f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__} - {str(ex)}.")
            exit()

        try:
            a = await self.get_chat_member(config.LOGGER_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("» قم برفـع البـوت مشـرفـاً بكافة الصلاحيات في مجموعـة السجـل")
                exit()
        except Exception as ex:
            LOGGER(__name__).error(f"Failed to verify bot's admin status in log group.\n  Reason : {type(ex).__name__} - {str(ex)}.")
            exit()

        LOGGER("ميوزك اليــكس").info(f"تم بدء تشغيل البوت {self.name} ...✓")

    async def stop(self):
        await super().stop()

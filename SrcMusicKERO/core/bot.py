import sys
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
        self.LOGGER_ID = config.LOGGER_ID

    async def start(self):
        try:
            await super().start()
            me = await self.get_me()
            self.id = me.id
            self.name = f"{me.first_name} {me.last_name or ''}".strip()
            self.username = me.username
            self.mention = me.mention

            if not self.LOGGER_ID:
                LOGGER(__name__).error("» خطأ: لم يتم تعيين معرف مجموعة السجل (LOGGER_ID) في config.py.")
                sys.exit(1)

            try:
                await self.send_message(
                    chat_id=self.LOGGER_ID,
                    text=f"<u><b>» تم تشغيل الميـوزك لـ البوت {self.mention} :</b></u>\n\n"
                         f"- ɪᴅ : <code>{self.id}</code>\n"
                         f"- ɴᴀᴍᴇ : {self.name}\n"
                         f"- ᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
                )
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("» قم باضافة البـوت مشـرفـاً بكافة الصلاحيات في مجموعة السجل")
                sys.exit(1)
            except Exception as ex:
                LOGGER(__name__).error(f"Bot has failed to access the log group/channel.\n  Reason: {type(ex).__name__} - {ex}.")
                sys.exit(1)

            try:
                chat_member = await self.get_chat_member(self.LOGGER_ID, self.id)
                if chat_member.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).error("» قم برفـع البـوت مشـرفـاً بكافة الصلاحيات في مجموعة السجل")
                    sys.exit(1)
            except Exception as ex:
                LOGGER(__name__).error(f"Failed to verify bot's admin status in log group.\n  Reason: {type(ex).__name__} - {ex}.")
                sys.exit(1)

            LOGGER("ميوزك اليــكس").info(f"تم بدء تشغيل البوت {self.name} ...✓")
        except Exception as ex:
            LOGGER("ميوزك اليــكس").error(f"فشل تشغيل البوت.\n  السبب: {type(ex).__name__} - {ex}")
            sys.exit(1)

    async def stop(self):
        await super().stop()

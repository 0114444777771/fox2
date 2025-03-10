from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
import config
from ..logging import LOGGER


class Zelzaly(Client):
    def __init__(self):
        LOGGER("ميوزك فوكس").info(f"جارِ بدء تشغيل البوت . . .")
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
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # التأكد من أن LOGGER_ID صالح
        try:
            logger_id = int(config.LOGGER_ID) if isinstance(config.LOGGER_ID, str) else config.LOGGER_ID
        except ValueError:
            LOGGER(__name__).error("❌ قيمة LOGGER_ID غير صحيحة! تأكد من إدخال رقم المجموعة بشكل صحيح.")
            exit()

        print(f"📌 يتم محاولة الوصول إلى مجموعة السجلات: {logger_id}")

        try:
            log_chat = await self.get_chat(logger_id)
            print(f"🔍 [DEBUG] نوع log_chat: {type(log_chat)} - البيانات: {log_chat}")

            if not hasattr(log_chat, "id"):
                raise AttributeError("لم يتم العثور على 'id' داخل كائن log_chat.")

            LOGGER("ميوزك فوكس").info(f"✅ تم الوصول إلى مجموعة السجلات: {log_chat.title}")

            await self.send_message(
                chat_id=log_chat.id,
                text=f"<u><b>» تم تشغيل الميـوزك لـ البوت {self.mention} :</b><u>\n\n"
                     f"- ɪᴅ : <code>{self.id}</code>\n"
                     f"- ɴᴀᴍᴇ : {self.name}\n"
                     f"- ᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "❌ قم بإضافة البوت كمشرف بكافة الصلاحيات في مجموعة السجلات!"
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"❌ فشل الوصول إلى مجموعة السجلات.\n"
                f"🔹 الخطأ: {type(ex).__name__} - {ex}"
            )
            exit()

        # التحقق من صلاحيات البوت في المجموعة
        try:
            chat_member = await self.get_chat_member(logger_id, self.id)
            if chat_member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "❌ قم برفع البوت مشرفًا بكافة الصلاحيات في مجموعة السجلات!"
                )
                exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"❌ حدث خطأ عند التحقق من صلاحيات البوت في مجموعة السجلات.\n"
                f"🔹 الخطأ: {type(ex).__name__} - {ex}"
            )
            exit()

        LOGGER("ميوزك فوكس").info(f"✅ تم بدء تشغيل البوت {self.name} بنجاح!")

    async def stop(self):
        await super().stop()

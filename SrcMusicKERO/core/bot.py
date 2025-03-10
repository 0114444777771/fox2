async def start(self):
    await super().start()
    self.id = self.me.id
    self.name = self.me.first_name + " " + (self.me.last_name or "")
    self.username = self.me.username
    self.mention = self.me.mention

    try:
        log_chat = await self.get_chat(config.LOGGER_ID)
        LOGGER("ميوزك فوكس").info(f"✅ تم الوصول إلى مجموعة السجلات: {log_chat.title}")

        await self.send_message(
            chat_id=config.LOGGER_ID,
            text=f"<u><b>» تم تشغيل الميـوزك لـ البوت {self.mention} :</b><u>\n\n- ɪᴅ : <code>{self.id}</code>\n- ɴᴀᴍᴇ : {self.name}\n- ᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
        )
    except (errors.ChannelInvalid, errors.PeerIdInvalid):
        LOGGER(__name__).error(
            "» قم باضافة البـوت مشـرفـاً بكافة الصلاحيات في مجموعـة السجـل"
        )
        exit()
    except Exception as ex:
        LOGGER(__name__).error(
            f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
        )
        exit()

    a = await self.get_chat_member(config.LOGGER_ID, self.id)
    if a.status != ChatMemberStatus.ADMINISTRATOR:
        LOGGER(__name__).error(
            "» قم برفـع البـوت مشـرفـاً بكافة الصلاحيات في مجموعـة السجـل"
        )
        exit()

    # ✅ ✅ ✅ تم تصحيح موضع هذا السطر ✅ ✅ ✅
    LOGGER("ميوزك فوكس").info(f" تم بدء تشغيل البوت {self.name} ...✓")


class Zelzaly(Client):
    pass  # تعريف الكلاس بدون مشاكل

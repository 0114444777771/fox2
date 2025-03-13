from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="FoxAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="FoxAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="FoxAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="FoxAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="FoxAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER.info("جـار تـشـغـيـل الـحـسـابـات الـمـسـاعـدة")

        for index, client in enumerate([self.one, self.two, self.three, self.four, self.five], start=1):
            if getattr(config, f"STRING{index}"):
                await client.start()
                try:
                    await client.join_chat("fox68899")
                    await client.join_chat("PX_CBL")
                    await client.join_chat("PX_CBL")
                except:
                    pass
                
                assistants.append(index)
                try:
                    await client.send_message(config.LOGGER_ID, f"» تم تشغيـل الحسـاب المسـاعـد {index} .. بنجـاح ✅")
                except:
                    LOGGER.error(f"حـدث خـطـأ اثـنـاء تـشـغـيـل الـحـسـاب المساعـد {index}، تأكـد أنـك أضفتـه لجـروب الإشـعـارات ورفـعـتـه أدمـن.")
                    exit()
                
                client.id = client.me.id
                client.name = client.me.mention
                client.username = client.me.username
                assistantids.append(client.id)
                LOGGER.info(f"تم بدء تشغيل الحساب المساعد {index}: {client.name} ...✓")

    async def stop(self):
        LOGGER.info("جـار إيـقـاف الـحـسـابـات الـمـسـاعـدة...")
        for index, client in enumerate([self.one, self.two, self.three, self.four, self.five], start=1):
            try:
                if getattr(config, f"STRING{index}"):
                    await client.stop()
            except:
                pass

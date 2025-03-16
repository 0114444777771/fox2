import asyncio
import importlib

from pyrogram import idle
NoActiveGroupCall = Exception  # مؤقتًا لتجنب الخطأ

import config
from SrcMusicKERO import LOGGER, app, userbot
from SrcMusicKERO.core.call import Zelzaly
from SrcMusicKERO.misc import sudo
from SrcMusicKERO.plugins import ALL_MODULES
from SrcMusicKERO.utils.database import get_banned_users, get_gbanned, maintenance_off
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER.error("كود جلسة الحساب المساعد غير مدعوم ...")
        exit()

    await sudo()

    # تعطيل وضع الصيانة
    await maintenance_off()
    LOGGER.info("✅ تم تعطيل وضع الصيانة بنجاح!")

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER.warning(f"حدث خطأ أثناء جلب المستخدمين المحظورين: {e}")

    await app.start()
    
    for all_module in ALL_MODULES:
        importlib.import_module(f"SrcMusicKERO.plugins.{all_module}")

    LOGGER.info("تم تحميل الإضافات ...✓")

    await userbot.start()
    await Zelzaly.start()

    try:
        await Zelzaly.stream_call("https://telegra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER.info(
            "خطأ .. قم بفتح المكالمة في مجموعة السجل الخاصة بك\n\nجارِ إيقاف بوت الميوزك . . ."
        )
        exit()
    except Exception as e:
        LOGGER.warning(f"حدث خطأ أثناء تشغيل المكالمة الصوتية: {e}")

    await Zelzaly.decorators()

    LOGGER.info("البوت يعمل بنجاح ✅")

    await idle()

    await app.stop()
    await userbot.stop()

    LOGGER.info("جارِ إيقاف بوت الميوزك . . .")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())

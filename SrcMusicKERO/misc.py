import socket
import time
import heroku3
from pyrogram import filters
import config
from SrcMusicKERO.core.mongo import mongodb
from .logging import LOGGER  # تأكد من أن LOGGER معرف بشكل صحيح

SUDOERS = set()  # ✅ تحسين: استخدام set() بدلًا من filters.user()
HAPP = None
_boot_ = time.time()

def is_heroku():
    """ تحديد ما إذا كان البوت يعمل على Heroku """
    return "heroku" in socket.getfqdn()

def dbb():
    """ تحديث قاعدة بيانات البوت """
    global db
    db = {}
    LOGGER.info("✅ تم تحديث قاعدة بيانات البوت بنجاح")

async def sudo():
    """ تحميل قائمة المطورين (SUDOERS) من قاعدة البيانات """
    global SUDOERS
    SUDOERS.add(config.OWNER_ID)  # إضافة المالك كـ sudo افتراضيًا
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = sudoers.get("sudoers", []) if sudoers else []

    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
        )

    SUDOERS.update(sudoers)
    LOGGER.info(f"✅ تم تحميل قائمة المطورين ({len(SUDOERS)} شخص)")

def heroku():
    """ إعداد الاتصال بـ Heroku وإضافة المتغيرات إذا لم تكن موجودة """
    global HAPP
    if not is_heroku():
        LOGGER.info("⚠️ البوت لا يعمل على Heroku، تجاوز إعدادات Heroku")
        return

    if not config.HEROKU_API_KEY or not config.HEROKU_APP_NAME:
        LOGGER.warning("⚠️ يرجى التأكد من ضبط متغيرات Heroku في config")
        return

    try:
        heroku_conn = heroku3.from_key(config.HEROKU_API_KEY)
        HAPP = heroku_conn.app(config.HEROKU_APP_NAME)
        heroku_var = HAPP.config()

        # إضافة المتغيرات إذا لم تكن موجودة
        default_vars = {
            "API_ID": "22624445",
            "API_HASH": "53bc68926ff18228dbbd89794211300b",
            "MONGO_DB_URI": "mongodb+srv://foxnasa603:admiNn12f@cluster0.6bcyg.mongodb.net/myDatabase?retryWrites=true&w=majority&appName=Cluster0",
        }

        added_vars = []
        for key, value in default_vars.items():
            if key not in heroku_var:
                heroku_var[key] = value
                added_vars.append(key)

        if added_vars:
            LOGGER.info(f"✅ تمت إضافة متغيرات البيئة: {', '.join(added_vars)}")
        else:
            LOGGER.info("✅ جميع متغيرات البيئة مضبوطة مسبقًا")

    except Exception as e:
        LOGGER.warning(f"⚠️ فشل الاتصال بـ Heroku: {e}")
